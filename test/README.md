# `agent-system-prompt-architect` 评估说明

这个目录用于回答两个问题，并把两类评估分开优化：

1. **触发是否准确**：skill frontmatter 里的 `description` 能不能让 Claude 或其他 agent harness 在该用时选择这个 skill，在不该用时跳过它。
2. **输出质量是否提升**：选中 skill 后，生成的可部署 system prompt 是否达到 `references/evaluation.md` 里的质量标准。

## 文件

- `evals.json`：输出质量评估用例。每个用例对应一个这个 skill 需要防住的失败模式，例如运行时实现细节泄漏、pipeline step 被当成角色、把示例值写死进规则等。
- `triggers.json`：触发评估用例。包含 should-trigger 和 should-not-trigger 查询，并拆成 train 60% 和 validation 40%，只用于调优 `description`。

## 自动化 runner

仓库提供了 `scripts/run_skill_evals.py`，可以通过 OpenAI-compatible chat endpoint 跑输出质量评估和触发评估。默认模型是 `mimo-v2.5-pro`。

在 shell 或本地 `.env` 文件中配置凭据，`.env` 已被 gitignore：

```powershell
$env:MIMO_API_KEY="..."
$env:MIMO_BASE_URL="https://token-plan-cn.xiaomimimo.com/v1"
$env:MIMO_MODEL="mimo-v2.5-pro"
```

安装依赖并跑 smoke test：

```powershell
uv sync
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --limit 1 --iteration smoke-001
```

跑完整 benchmark：

```powershell
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --iteration full-001
```

只跑单个 case，多个 case 可以重复传 `--case`：

```powershell
uv run python scripts\run_skill_evals.py --quality --case abstract-minimal-input --iteration ad-hoc-001
```

结果会写入 `evals-workspace/<iteration>/`，包括每个 case 的输出、耗时、评分证据、触发判断和聚合后的 `benchmark.json`。

## 运行产物结构

测试定义放在 `test/`，运行产物放在 gitignore 的 `evals-workspace/`。这样 skill 安装目录保持干净。

```text
agent-system-prompt-architect-skill/
├── skills/
│   └── agent-system-prompt-architect/
│       ├── SKILL.md
│       └── references/...
├── test/
│   ├── evals.json
│   ├── triggers.json
│   └── README.md
└── evals-workspace/                  # gitignored
    └── iteration-<N>/
        ├── <eval-id>/
        │   ├── with_skill/
        │   │   ├── outputs/          # 生成的 system prompt 和额外输出
        │   │   ├── timing.json       # { "total_tokens": ..., "duration_ms": ... }
        │   │   └── grading.json      # { "assertion_results": [...], "summary": {...} }
        │   └── without_skill/
        │       ├── outputs/
        │       ├── timing.json
        │       └── grading.json
        └── benchmark.json            # 当前 iteration 的聚合统计
```

`with_skill` 会加载 `SKILL.md` 和 skill 选择读取的 references。`without_skill` 使用同一个模型和同一个用户请求，但不加载 skill，用来判断 skill 是否真的带来了增益。

## 输出质量评估怎么跑

对 `evals.json` 里的每个 `eval`：

1. **生成输出**。用一个干净 agent 运行下面的请求，并把完整最终响应保存到 `outputs/system_prompt.md`。

   ```text
   You are about to act on a real user request. Use the skill at <SKILL_PATH> if applicable.

   User request:
   <eval.prompt>

   Save the final deliverable system prompt to <outputs_dir>/system_prompt.md.
   ```

   同时用不加载 skill 的方式跑同一个 `<eval.prompt>`，保存到 `without_skill/outputs/system_prompt.md`。

2. **记录耗时和 token**。写入 `timing.json`：

   ```json
   { "total_tokens": 0, "duration_ms": 0 }
   ```

3. **评分**。对每条 assertion 写入 `grading.json`。`passed: true` 必须有具体证据。条件断言如果不适用于当前输出，记录为 `applicable: false`，并从 `total` 和 `pass_rate` 中排除：

   ```json
   {
     "assertion_results": [
       { "text": "<assertion>", "applies_when": null, "applicable": true, "passed": true, "evidence": "outputs/system_prompt.md 中的原文引用或位置" },
       { "text": "<assertion>", "applies_when": "the response drafts a prompt", "applicable": false, "passed": null, "evidence": "skipped: response is clarification-only" }
     ],
     "summary": { "passed": 0, "failed": 0, "skipped": 0, "total": 0, "pass_rate": 0.0 }
   }
   ```

4. **聚合**。把每个 eval 的评分汇总到 `benchmark.json`：

   ```json
   {
     "run_summary": {
       "with_skill":    { "pass_rate": { "mean": 0.0, "stddev": 0.0 }, "tokens": { "mean": 0, "stddev": 0 } },
       "without_skill": { "pass_rate": { "mean": 0.0, "stddev": 0.0 }, "tokens": { "mean": 0, "stddev": 0 } },
       "delta": { "pass_rate": 0.0, "tokens": 0 }
     }
   }
   ```

## 断言类型

`evals.json` 里的大部分断言都应该先尝试用 substring 或 regex 检查；如果无法可靠用字符串判断，再交给 LLM judge。

示例：

- `does not contain the substring 'PushMessageDraft'`：字符串检查。
- `the role line contains at least one profession-style noun from the set {...}`：在角色行做词表检查。
- `the missing-input rule asks the agent to say what is missing and skip generation`：LLM judge，并引用相关段落作为证据。

### 条件断言

有些断言只适用于某一种合法输出形态。例如“角色名称必须是专业身份”只适用于响应里已经起草了 system prompt；如果响应只是提出澄清问题，这条断言没有意义。

这种情况用对象形式，而不是纯字符串：

```json
{
  "text": "The drafted prompt names a real professional role and a specific domain",
  "applies_when": "the response contains a drafted system prompt for the target agent (not just clarification questions)"
}
```

LLM grader 会先判断 `applies_when` 是否成立。如果不成立，这条断言标记为 `applicable: false`，不计入该 case 的 `total` 和 `pass_rate`。这样可以避免一个本来合法的替代路径被错误扣分。

纯字符串断言仍然可用，并视为总是适用。只有当断言本身需要写成 “If ...” 或对某个合法输出形态无意义时，才使用条件断言。

## 触发评估怎么跑

`triggers.json` 用来调 skill 的 `description`，不是调正文。对每个 query：

1. 给一个干净 agent 提供所有可用 skill 的 metadata，也就是 name + description，不加载 `SKILL.md` 正文。
2. 让 agent 判断当前 query 应该使用哪个 skill，或者不使用任何 skill。记录当前 skill 的 `selected: true|false`。
3. 和 `should_trigger` 对比，分别计算 train 和 validation 的通过率。
4. 如果要修改 description：
   - 只用 train failures 驱动修改。
   - validation 只用于验证最终 description 是否泛化。
   - description 保持在 1024 字符以内。
   - 不要把失败 query 里的具体关键词硬塞进去，要抽象出背后的触发概念。

## 评分原则

这些原则同时适用于 `evals.json` 和 `triggers.json`：

- **PASS 必须有具体证据**。例如只有一个标题叫 “Output contract”，但内容是一句空话，不能算满足“描述输出格式、字段标签和完成标准”。评分时要引用具体行作为证据。
- **检查断言本身是否有价值**。如果某条断言在 `with_skill` 和 `without_skill` 里总是都通过，它可能没有测出 skill 价值；如果总是都失败，可能断言坏了或太严；如果无法从保存输出验证，也应该重写。
- **从失败模式泛化**。如果多个 eval 都出现同类失败，例如 schema 名泄漏、角色变成“动词 + 代理”，优先修 `SKILL.md` 或 reference 里的底层规则，而不是给单个 case 打补丁。

## 迭代流程

1. 在 iteration `N` 里跑完所有 `evals.json` case，并同时生成 `with_skill/` 和 `without_skill/`。
2. 汇总 `benchmark.json`，看 skill 相对 baseline 的 pass rate delta。
3. 检查失败，选择一种处理：
   - 修改 `SKILL.md` 或 reference，解决可泛化的失败模式。
   - 放宽或重写不可验证、太脆或误伤合法输出的 assertion。
   - 如果出现真实失败但现有 eval 抓不到，补一个新 case。
4. 进入 iteration `N+1`，重新评估。
5. 当通过率平台化，或者关键失败模式在 validation 上清零时停止。

## 什么时候新增或修改测试用例

新增 case：

- 真实使用中出现了现有 case 抓不到的新失败模式。
- 某个 reference 新增了规则，需要实证信号确认它真的改变行为。

重写 assertion：

- 它不管 skill 好坏都会通过。
- 它过度依赖精确短语，导致同样正确的输出被误判。
- 它无法仅凭保存的输出验证。

不要因为“看起来可以更完整”就加 case。每个 case 都有 token 成本和评分时间成本。
