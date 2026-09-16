# 发布说明

## v0.2 - 2026-09-16

对照 Agent Skills 开放标准（agentskills.io）和最新 skill 编写指南做的一次规范化维护。

### 改进

- 安装路径更新为 Codex 新约定：`~/.agents/skills`（用户级）与 `.agents/skills`（仓库级），旧版 `~/.codex/skills` 保留说明；新增 Claude Code 等兼容平台的安装提示。
- `description` 改写为第三人称能力陈述 + 触发场景结构，补充中文触发词（系统提示词、角色设定、提示词改写等）和负向触发边界，提升跨模型触发稳定性。
- frontmatter 补充 `license: MIT`，与仓库 LICENSE 一致。
- README 参考链接新增 Agent Skills 开放标准。

### 文档

- 新增 `README.en.md` 英文版首页，与中文 README 顶部互相链接实现语言切换（GitHub 会剥离 Markdown 中的脚本，双文件是社区标准做法），仓库结构章节同步补充。

### 移除

- 移除自动化评估体系（`test/`、`scripts/`、`pyproject.toml`、`uv.lock`）：回归主流 skill 形态，评估不再随仓库分发。
- skill 内部的写作质量检查清单 `references/evaluation.md` 保留不变，它属于 skill 功能本体（初稿自检流程），不受影响。

## v0.1 - 2026-05-21

首个公开版本，重点是把 skill 从“能生成系统提示词”推进到“能稳定生成可部署、可评估、少幻觉的 agent 系统提示词”。

### 新增

- 新增 MIMO 兼容的自动化评估 runner：支持质量评估、触发评估、baseline 对照、单 case 运行和迭代结果归档。
- 新增 `test/` 评估资产：包含输出质量用例、触发用例和评估说明。
- 新增 `uv` 项目配置，方便一条命令安装依赖并运行评估。

### 改进

- 强化默认交付模式：默认直接输出可部署 system prompt，避免额外设计说明混入最终提示词。
- 强化 prompt engineering 原则：更强调明确目标、正向指导、格式样例、判断标准和可执行替代行为。
- 强化运行时隔离：避免把 schema 字段、class 名、上下游管线词、业务代号直接写进目标 agent 的提示词。
- 强化角色命名规则：默认使用职责和专业领域定义角色，而不是项目名、品牌名或 pipeline step 名。
- 强化工具契约规则：只有真实 runtime spec 存在时才写具体工具名、参数和返回字段；只有语义能力时不虚构 API。
- 强化内部评估流程：写完初稿后先按 `references/evaluation.md` 做质量检查，再压缩和修正。

### 文档与结构

- README 改为中文项目首页，补充适用场景、核心问题、安装方式、使用示例、评估结果和设计思路。
- `test/README.md` 改为中文评估说明，保留 runner 用法、断言规则和迭代流程。
- skill 正文和 reference 文件仍保持英文，便于 agent 在运行时稳定理解和执行。
- 将评估定义放在仓库根目录 `test/`，避免把测试资产混进可安装 skill 目录。
- 更新 `.gitignore`，忽略 `.env` 和 `evals-workspace/`，避免提交本地密钥和评估输出。
