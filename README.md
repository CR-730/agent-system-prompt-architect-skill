# Agent System Prompt Architect Skill

[![License: MIT](https://img.shields.io/github/license/CR-730/agent-system-prompt-architect-skill)](LICENSE)
[![Release](https://img.shields.io/github/v/release/CR-730/agent-system-prompt-architect-skill?label=release)](https://github.com/CR-730/agent-system-prompt-architect-skill/releases)
[![Skill](https://img.shields.io/badge/Codex-Skill-blue)](skills/agent-system-prompt-architect/SKILL.md)
[![Standard](https://img.shields.io/badge/Agent%20Skills-标准-brightgreen)](https://agentskills.io/specification)
[![Docs](https://img.shields.io/badge/docs-中文-brightgreen)](README.md)

感谢佬的 star，初来乍到可能很多地方不规范，有问题或者建议可以在 issues 跟我提(非常欢迎)，我会尽快跟进。

这是一个让 Codex / code agent 学会为 agent 项目编写高质量系统提示词的 skill。

起因是我在用 Codex 写 agent 项目时，经常遇到它生成的系统提示词完全不规范的问题，因此结合一些参考资料编写了这个 skill。

## 目录

- [适合什么场景](#适合什么场景)
- [解决什么问题](#解决什么问题)
- [核心能力](#核心能力)
- [安装](#安装)
- [使用示例](#使用示例)
- [仓库结构](#仓库结构)
- [核心设计](#核心设计)
- [参考](#参考)

## 适合什么场景

当你想让 agent 帮你写另一个 agent 的 system prompt 时，可以使用这个 skill。

不适合的场景：
- 只想随手写一句普通 prompt
- 目标不是 agent system prompt，而是营销文案、文章、脚本或普通聊天提示词

## 解决什么问题

很多 agent 写 prompt 时容易出现这些问题：

- 把项目名、品牌名、业务代号当成角色名，例如你是小红薯 agent
- 喜欢把后端代码名词直接写进 system prompt
- 喜欢说不要做什么，没有清晰的规范和约束
- 明明没有真实工具定义，却虚构工具名、参数和返回字段
- 把一段系统提示词写得很长，却没有分层结构

## 核心能力

- 生成可直接放进 agent 的系统提示词
- 设计清晰的角色、任务范围、非目标和失败处理
- 减少模型幻觉输出
- 区分语义工具能力和真实运行时工具规格
- 处理资料来源、检索、引用、证据冲突和不确定性
- 应用提示词工程标准原则：具体指令、正向引导、格式示例、可衡量成功标准
- 按需选择高阶提示技术：few-shot、reasoning policy、ReAct-style tool use、retrieval grounding
- 写完初稿后按 `references/evaluation.md` 内部检查，再压缩和修正

## 安装

推荐按 [.codex/INSTALL.md](.codex/INSTALL.md) 安装，它包含 macOS / Linux / Windows 的 clone、链接、验证、更新和卸载步骤，以及仓库级安装（`.agents/skills/`）和其他平台（如 Claude Code）的说明。

快速复制安装（用户级，当前 Codex 约定路径）：

```powershell
$dest = "$env:USERPROFILE\.agents\skills\agent-system-prompt-architect"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
if (Test-Path $dest) {
  Write-Error "Skill already exists: $dest"
  exit 1
}
Copy-Item -Recurse -Path .\skills\agent-system-prompt-architect -Destination "$env:USERPROFILE\.agents\skills"
```

> 旧版本 Codex 的 skill 目录是 `~/.codex/skills`，如果你的版本较旧，把上面命令里的 `.agents` 换成 `.codex`。

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
├── RELEASE-NOTES.md
└── README.md
```

## 核心设计
1. 将提示词工程标准规则和高阶技术拆成独立参考文件，让 agent 先按基础范式写，再按场景选择 few-shot、推理策略、ReAct 式工具使用、检索增强等技术。
2. 写完初稿后，用评估清单做内部质量检查，再压缩、合并重复规则、修正不可部署内容。
3. 引入领域适配清单，让 agent 根据目标用户、任务、资料来源、工具副作用、输出格式和安全边界做领域适配。
4. 把具体代码名词翻译成 agent 可执行的行为规则。
5. 针对多类 agent 能力提供标准模板，如检索增强、代码执行、客服支持、研究分析等场景。

## 参考

- [Agent Skills 开放标准](https://agentskills.io/specification)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [Prompt Engineering Notes](https://www.aneasystone.com/archives/2024/01/prompt-engineering-notes.html)

## License

MIT
