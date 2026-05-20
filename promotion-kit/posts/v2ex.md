标题：开源了一个帮 Agent 写 System Prompt 的 Skill，想听听大家意见

最近做了一个小工具/skill：Agent System Prompt Architect

GitHub：
https://github.com/CR-730/agent-system-prompt-architect-skill

它不是“万能提示词合集”，而是一个给 Codex / Claude Code 这类 agent 用的 skill，用来生成可直接部署的 system prompt。

背景是我发现让 AI 给另一个 agent 写 prompt 时，很容易出几个问题：

- 项目名叫 xxx，就自动写成“你是 xxx 的审计人”
- 只说有“检索/保存”工具能力，它就编出一套假 API
- prompt 越写越长，安全、工具、失败处理重复出现
- 把经验偏好写成硬规则，反而限制 agent 自己选择最短路径

所以这个 skill 主要做了几件事：

- 名称只当标签，不直接推导角色
- 区分稳定事实和经验判断
- 语义工具能力只写行为规则，不编工具名/参数/返回字段
- 默认只输出 system prompt，不输出 JSON 包
- 用 evaluation 清单做一轮压缩和去重
- 把 Few-shot / ReAct / RAG / Step-back 等技术做成可选策略，而不是默认全塞

目前仓库结构参考了 anthropics/skills、superpowers 这类 skill repo：

```
skills/agent-system-prompt-architect/
  SKILL.md
  references/
```

欢迎大家拍砖，尤其想听听：skill 应该写多详细，才不会把 agent 锁死？
