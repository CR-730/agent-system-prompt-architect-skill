# 开源项目：Agent System Prompt Architect Skill

项目地址：  
https://github.com/CR-730/agent-system-prompt-architect-skill

这是一个用于 Codex / Claude Code 风格 agent 的 Skill，目标是帮助 agent 生成可直接部署的 system prompt。

它关注的问题：

- 避免从项目名直接推导错误角色
- 避免把语义工具能力写成假 API
- 避免 system prompt 过长和重复
- 避免把经验偏好写成固定执行路径
- 让最终 prompt 更适合直接放入 system message

主要文件：

- `SKILL.md`：主技能说明
- `prompt-engineering-principles.md`：基础提示词原则
- `prompt-techniques.md`：Few-shot、ReAct、RAG 等技术选择表
- `domain-adaptation.md`：领域适配清单
- `evaluation.md`：提示词质量检查清单

适合正在做 AI Agent、工具型 Agent、Claude Code/Codex Skill 的开发者参考。

欢迎 star、issue 和建议。
