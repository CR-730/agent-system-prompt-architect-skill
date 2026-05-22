# 评估说明

用来验证 skill 是否真的能让 agent 写出更好的系统提示词。

评估目前只关注已经在实际使用中出现过、并且值得防止的失败模式。

## 评估什么

这里分两类检查：

- **输出质量**：使用 skill 后，生成的系统提示词是否更清晰、更可部署、更少编造工具或照搬代码实现细节。
- **触发准确性**：当用户需要设计、修改或评审 agent system prompt 时，agent 是否会选择这个 skill；无关任务是否会跳过它。

## 文件

- `evals.json`：质量测试用例。每条用例都对应一个具体失败模式。
- `triggers.json`：触发测试用例。用于检查 skill 的描述是否容易被正确选中。
- `../scripts/run_skill_evals.py`：自动运行评估的脚本。

本地运行结果会写到 `evals-workspace/`，这个目录不会提交到仓库。

## 快速运行

先配置模型接口：

```powershell
$env:MIMO_API_KEY="..."
$env:MIMO_BASE_URL="https://token-plan-cn.xiaomimimo.com/v1"
$env:MIMO_MODEL="mimo-v2.5-pro"
```

安装依赖并跑一个最小测试：

```powershell
uv sync
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --limit 1 --iteration smoke-001
```

跑完整评估：

```powershell
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --iteration full-001
```

只跑某一条质量用例：

```powershell
uv run python scripts\run_skill_evals.py --quality --case abstract-minimal-input --iteration ad-hoc-001
```

## 怎么看结果

每轮结果会放在：

```text
evals-workspace/<本轮名称>/
```

最重要的是 `benchmark.json`，它会汇总本轮通过率。你主要看：

- 使用 skill 的结果是否高于不使用 skill 的结果。
- 失败项是不是集中在同一种问题上。
- 修改 skill 后，同类失败是否减少，而不是只修好了某一个样例。

每条用例下面也会保存模型生成的系统提示词和评分证据。需要排查失败时，再打开对应目录查看。

## 测试用例怎么写

新增用例时，先写清楚它要防止什么失败，而不是为了“更完整”而加测试。

适合新增用例的情况：

- 真实使用中出现了新的失败模式。
- skill 新增或修改了一条关键规则，需要验证它是否真的生效。
- 现有测试无法覆盖某类重要行为。

不适合新增用例的情况：

- 只是想把文档写得更完整。
- 只是想覆盖某个具体关键词。
- 这个问题已经能被现有用例测到。

## 评分原则

评分要看实际输出，一条通过判断应该满足：

- 能在生成结果里找到具体证据。
- 不依赖某个固定措辞。
- 不惩罚合法替代路径，例如先澄清、明确假设、或省略不必要模块。

如果一条判断对使用 skill 和不使用 skill 的结果都没有区分度，就应该重写或删除。

## 维护原则

修改顺序建议：

1. 先看失败是否代表真实问题。
2. 如果是真问题，优先修改 `SKILL.md` 或 `references/` 里的通用规则。
3. 如果是评分误伤，再调整测试判断。
4. 如果现有用例抓不到新问题，再补新用例。

不要为单个样例硬编码规则，每次修改都应该能解释为解决一类可复现的问题。
