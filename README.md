# Agent System Prompt Architect Skill

感谢佬的 star，初来乍到可能很多地方不规范，有问题或者建议可以在 issues 跟我提(非常欢迎)，我会尽快跟进。

这是一个让 Codex / code agent 学会为 agent 项目编写高质量系统提示词的 skill。

起因是我在用 Codex 写 agent 项目时，经常遇到它生成的系统提示词完全不规范的问题，因此结合一些参考资料编写了这个 skill。

## 适合什么场景

当你想让 agent 帮你写另一个 agent 的 system prompt 时，可以使用这个 skill，例如：

- 客服 agent、学习助手 agent、研究 agent、代码执行 agent
- 需要工具调用、检索、引用、保存记录、审批确认的 agent
- 需要明确输出格式、安全边界、失败处理和自检标准的 agent
- 需要把产品需求、接口说明、工具能力说明转成可部署提示词的场景

不适合的场景：

- 只想随手写一句普通 prompt
- 已经有完整系统提示词，只需要改几个文案词
- 目标不是 agent system prompt，而是营销文案、文章、脚本或普通聊天提示词

## 解决什么问题

很多 agent 写 prompt 时容易出现这些问题：

- 把项目名、品牌名、业务代号当成角色名，例如“你是某某 App agent”
- 把后端 schema、class 名、字段名、上下游管线词直接写进 system prompt
- 只有抽象禁令，没有明确目标、输出格式、判断标准和替代行为
- 明明没有真实工具 schema，却虚构工具名、参数和返回字段
- 把一段系统提示词写得很长，但没有可执行的任务边界
- 输出最终 prompt 之前夹带设计说明或供你审阅等不可部署内容

这个 skill 会强制 agent 把这些信息转成面向目标 agent 的行为规则，而不是照搬运行时实现细节。

## 核心能力

- 生成可直接放进 system message 的系统提示词
- 设计清晰的角色、任务范围、非目标和失败处理
- 区分语义工具能力和真实运行时工具规格
- 对真实工具写可执行工具契约：使用时机、输入、返回、缺参处理、结果校验
- 在没有真实工具 schema 时，不虚构 API、参数或返回字段
- 处理资料来源、检索、引用、证据冲突和不确定性
- 应用 prompt engineering 原则：具体指令、正向引导、格式示例、可衡量成功标准
- 按需选择高阶提示技术：few-shot、reasoning policy、ReAct-style tool use、retrieval grounding
- 写完初稿后按 `references/evaluation.md` 内部检查，再压缩和修正

## 安装

推荐按 [.codex/INSTALL.md](.codex/INSTALL.md) 安装，它包含 macOS / Linux / Windows 的 clone、链接、验证、更新和卸载步骤。

快速复制安装：

```powershell
$dest = "$env:USERPROFILE\.codex\skills\agent-system-prompt-architect"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills"
if (Test-Path $dest) {
  Write-Error "Skill already exists: $dest"
  exit 1
}
Copy-Item -Recurse -Path .\skills\agent-system-prompt-architect -Destination "$env:USERPROFILE\.codex\skills"
```

安装后重启 Codex，让它重新发现 skill。

## 使用示例

```text
请使用 $agent-system-prompt-architect

我想做一个中文学习助手 agent，主要给高中生和大学低年级学生用。
它需要能解释课程知识点、根据用户上传资料回答问题、整理错题、制定复习计划。
系统里可能会有检索用户资料、检索课程知识库、保存错题、生成学习计划等工具，
但我还没有确定真实工具名、参数和返回格式。

帮我写一个可以直接放进 system message 的系统提示词。
```

如果你只是探索想法，可以这样问：

```text
请使用 $agent-system-prompt-architect

我想做一个面向企业知识库的问答 agent。
先帮我判断它的系统提示词应该包含哪些模块，不要急着写完整 prompt。
```

## 评估

本仓库带有自动化评估用例和 runner，用于比较使用 skill和不使用 skill的差异。

当前内部基准结果：

- 模型：`mimo-v2.5-pro`
- 质量评估：with skill 平均通过率 `0.917`，without skill 平均通过率 `0.554`
- 触发评估：14 / 14 通过
- 结果文件：`evals-workspace/iteration-006/benchmark.json`

运行 smoke test：

```powershell
uv sync
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --limit 1 --iteration smoke-001
```

完整评估说明见 [test/README.md](test/README.md)。

## 仓库结构

```text
agent-system-prompt-architect-skill/
├── .codex/
│   └── INSTALL.md
├── skills/
│   └── agent-system-prompt-architect/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── references/
│           ├── prompt-engineering-principles.md
│           ├── prompt-techniques.md
│           ├── domain-adaptation.md
│           ├── evaluation.md
│           ├── rag_template.md
│           ├── code_agent_template.md
│           ├── support_agent_template.md
│           ├── research_agent_template.md
│           ├── snippets.md
│           └── template.md
├── test/
│   ├── evals.json
│   ├── triggers.json
│   └── README.md
├── scripts/
│   └── run_skill_evals.py
├── RELEASE-NOTES.md
└── README.md
```

## 设计思路

这个 skill 的核心是让 agent 学会在写系统提示词时做几件关键判断：

1. 哪些内容是目标 agent 必须执行的固定规则。
2. 哪些内容只是用户给出的示例、schema、项目名或运行时实现细节。
3. 哪些工具信息可以写成真实工具契约，哪些只能写成语义使用规则。
4. 哪些 prompt engineering 技术真的会改变行为，哪些只是增加长度。
5. 最终输出是否能直接部署，而不是还需要用户二次清理。

## 参考

- [Anthropic Skills](https://github.com/anthropics/skills)
- [Prompt Engineering Notes](https://www.aneasystone.com/archives/2024/01/prompt-engineering-notes.html)

## License

MIT
