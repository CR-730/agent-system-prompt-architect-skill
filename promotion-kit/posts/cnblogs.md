# 开源一个用于生成 Agent System Prompt 的 Skill

项目地址：  
https://github.com/CR-730/agent-system-prompt-architect-skill

最近在整理 AI Agent 的 system prompt 写法时，发现一个问题：提示词写得越详细，不一定效果越好。

有时我们写进去的是“经验推断”，比如“优先走 UI”“像人一样浏览网页”“工具通道二选一”。这些话本意是帮助 agent，但模型可能会把它们当成硬规则，反而降低执行效率。

所以我做了一个 skill：Agent System Prompt Architect。

它的核心原则：

- 写稳定事实和判断标准，不把经验偏好写成固定执行路径
- 从任务、用户、职责和成功标准推导角色，不从项目名推导角色
- 区分语义工具能力和真实 runtime tool spec
- 不编工具名、参数和返回字段
- 默认输出可部署 system prompt
- 用 evaluation 清单做压缩和去重

这个仓库也包含一些参考文件：

- prompt engineering 基础原则
- prompt techniques 选择表
- domain adaptation 清单
- RAG / code / support / research 能力模块

欢迎交流：给 agent 写 skill，到底应该写多详细？
