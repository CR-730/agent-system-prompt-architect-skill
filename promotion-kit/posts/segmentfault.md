# 开源：Agent System Prompt Architect，一个生成可部署 System Prompt 的 Skill

项目地址：  
https://github.com/CR-730/agent-system-prompt-architect-skill

## 背景

在写 agent 项目时，经常需要让 AI 生成 system prompt。但直接让 AI 写，容易出现这些问题：

- 根据项目名过度推断角色
- 把语义工具能力写成不存在的 API
- 输出很长，规则重复，优先级不清楚
- 把经验偏好写成固定执行路径
- 中文 prompt 里混入英文标签

## 这个 Skill 做什么

Agent System Prompt Architect 是一个 Codex/Claude Code 风格的 skill，用来生成可直接部署的 system prompt。

它强调：

- 角色从任务、用户、职责、成功标准推导，而不是从项目名推导
- 工具能力和真实工具规格分开
- 默认输出 system prompt，不输出 JSON/schema/package wrapper
- 领域适配用 checklist，不堆领域模板
- 通过 evaluation 清单做一次压缩和去重
- Few-shot、ReAct、RAG、Step-back 等作为可选策略使用

## 结构

```text
skills/agent-system-prompt-architect/
  SKILL.md
  references/
    prompt-engineering-principles.md
    prompt-techniques.md
    domain-adaptation.md
    evaluation.md
```

欢迎试用和反馈。
