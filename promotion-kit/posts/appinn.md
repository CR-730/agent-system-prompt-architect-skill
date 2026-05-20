标题：分享一个开源 Agent Skill：帮 AI 写更好的 System Prompt

我做了一个小工具，适合在 Codex / Claude Code 这类 agent 环境里使用：

https://github.com/CR-730/agent-system-prompt-architect-skill

它的作用是：让 AI 帮你写另一个 AI Agent 的 system prompt。

我做这个的原因是，直接让 AI 写提示词时，经常会出现：

- 根据项目名乱写角色
- 把“有检索工具”写成一套不存在的 API
- 提示词越写越长，规则重复
- 把经验判断写成固定步骤，限制 agent 自己选择更短路径

这个 skill 会提醒 agent：

- 名称只是标签，不是角色
- 工具能力不等于真实工具接口
- 默认输出可直接使用的 system prompt
- 写完后要压缩、去重、检查边界和输出格式

不是面向普通聊天的提示词合集，更偏开发者工具。

欢迎试用和提建议。
