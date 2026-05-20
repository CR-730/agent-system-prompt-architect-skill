标题：开源分享：一个帮 Agent 写 System Prompt 的 Skill

最近在整理一个给 Codex / Claude Code 用的 skill：

https://github.com/CR-730/agent-system-prompt-architect-skill

用途很单一：让 agent 帮你写另一个 agent 的 system prompt。

不是提示词合集，也不是套模板生成器。主要想解决这些问题：

- AI 根据项目名乱推角色，比如项目名叫 xxx，就写“你是 xxx 的审计人”
- 用户只说有工具能力，AI 就编出工具名、参数、返回字段
- system prompt 写得太长，安全、工具、失败处理重复很多遍
- 把经验判断写成硬规则，导致 agent 不会选择更短更可靠的路径

这个 skill 目前的原则：

- 默认输出可直接放进 system message 的 prompt
- 工具能力和真实 runtime spec 分开
- 只在真实工具规格存在时写工具契约
- 领域适配用清单，不做垂直领域模板库
- prompt 技术是可选策略，不默认堆 CoT/Few-shot/ReAct
- 写完后按 evaluation 清单压缩一次

欢迎试用，也欢迎提 issue。  
我主要想验证一个问题：给 agent 写 skill，到底应该提供多少“经验”，才不会反过来限制它？
