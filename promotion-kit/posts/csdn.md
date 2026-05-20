# Agent System Prompt Architect：一个帮 AI Agent 写系统提示词的 Skill

GitHub：  
https://github.com/CR-730/agent-system-prompt-architect-skill

## 项目简介

Agent System Prompt Architect 是一个面向 Codex / Claude Code 风格环境的 Skill，用于生成可部署的 Agent System Prompt。

它不是提示词合集，而是一个提示词架构 skill。

## 解决的问题

让 AI 直接写 system prompt 时，常见问题包括：

1. 根据项目名乱推角色  
2. 把工具能力写成不存在的 API  
3. 生成过长、重复的提示词  
4. 把经验偏好变成固定流程  
5. 缺少对领域、工具、证据、输出格式的判断标准  

## 核心设计

- 名称只作为标签，不直接作为角色
- 稳定事实和判断标准优先
- 工具能力和真实工具规格分离
- 默认输出 system prompt
- 领域适配用 checklist
- prompt 技术按需选择
- 写完后用 evaluation 清单压缩和审查

## 目录结构

```text
skills/agent-system-prompt-architect/
  SKILL.md
  agents/openai.yaml
  references/
```

如果你也在做 AI Agent 或提示词工程，可以参考这个项目。
