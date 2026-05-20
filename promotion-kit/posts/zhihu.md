# 如何让 AI 帮另一个 Agent 写出更好的 System Prompt？

我最近开源了一个小项目：**Agent System Prompt Architect Skill**  
仓库： https://github.com/CR-730/agent-system-prompt-architect-skill

它的目标不是收集一堆万能提示词，而是解决一个更具体的问题：

> 当我们让 AI 给另一个 agent 写 system prompt 时，怎样避免它写得又长、又假、又容易限制 agent？

我在迭代时遇到几个典型反例：

1. 项目名叫 xxx，AI 直接写“你是 xxx 的审计人”  
   这其实是把“名称”当成了“角色”，而不是从任务、用户、职责和成功标准推导角色。

2. 用户只说“有检索资料、保存记录这些工具能力”，AI 却编出工具名、参数、返回字段  
   这会让 system prompt 看起来很工程化，实际上是假 API。

3. 为了完整，把安全、隐私、工具失败、学术诚信等规则重复写很多遍  
   最后 prompt 很长，优先级反而不清楚。

这个 skill 的核心取向是：

- 把名称当标签，不当角色
- 把稳定事实和判断标准写清楚
- 避免把经验偏好变成固定执行路径
- 语义工具只写行为规则，真实工具规格才写可执行契约
- 默认生成可部署 system prompt，而不是 JSON 包
- 生成后用 evaluation 清单压缩、去重、修正

它也把一些常见 prompt 技术做成“选择表”，比如 Few-shot、Step-back、ReAct、RAG、Self-consistency，而不是默认都塞进 prompt。

如果你也在做 agent prompt、Claude Code skill、Codex skill，欢迎看看这个仓库：  
https://github.com/CR-730/agent-system-prompt-architect-skill

我也想听听大家对“给 agent 写 skill 到底该写多详细”的看法。
