# 我开源了一个用于编写 Agent System Prompt 的 Skill：Agent System Prompt Architect

最近在反复打磨一个 Codex/Claude Code 可用的 Agent Skill：  
**Agent System Prompt Architect**

仓库地址：  
https://github.com/CR-730/agent-system-prompt-architect-skill

它解决的问题很具体：当我们让 AI 给另一个 agent 写 system prompt 时，AI 经常会出现几个问题：

- 把项目名直接推成角色，比如项目叫 xxx，就写“你是 xxx 的审计人”
- 把语义工具能力写成假 API，编出工具名、参数、返回字段
- 为了“完整”把 prompt 写得特别长，重复堆安全规则和工具规则
- 把经验偏好写成硬路径，限制 agent 自己选择最短可靠路径
- 中文需求里混入英文 section tag

这个 skill 现在的设计原则是：

- 默认输出可直接放进 system message 的系统提示词
- 不输出 JSON 包、schema 包装或假工具接口
- 区分“稳定事实”和“经验判断”
- 用领域适配清单，而不是堆垂直领域模板
- 工具规则区分“语义能力”和“真实 runtime spec”
- 生成后用 evaluation 清单做一次自检和压缩

仓库里包含：

- `SKILL.md`：主技能说明
- `references/prompt-engineering-principles.md`：基础提示词原则
- `references/prompt-techniques.md`：CoT、Few-shot、ReAct、RAG 等技术的选择表
- `references/domain-adaptation.md`：领域适配清单
- `references/evaluation.md`：系统提示词质量检查清单

我自己的目标不是做一个“提示词大全”，而是做一个能帮 agent 写出更稳、更短、更可部署 system prompt 的技能。

欢迎试用和提 issue。
