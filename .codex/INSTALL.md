# 为 Codex 安装 Agent System Prompt Architect Skill

通过 Codex 原生 skill 发现机制安装本仓库的 `agent-system-prompt-architect` skill。推荐使用符号链接或 Windows 目录连接，这样后续 `git pull` 后可以即时更新。

> 路径说明：当前 Codex 的 skill 目录约定是 `~/.agents/skills`（用户级）和仓库内的 `.agents/skills`（仓库级）。旧版本 Codex 使用 `~/.codex/skills`，如果你的 Codex 版本较旧，把下文命令里的 `.agents` 替换为 `.codex` 即可。

## 前置条件

- Git
- Codex 已安装并能读取用户目录下的 skills

## 安装步骤

### macOS / Linux

1. 克隆仓库：

   ```bash
   repo="$HOME/.agents/agent-system-prompt-architect-skill"
   git clone https://github.com/CR-730/agent-system-prompt-architect-skill.git "$repo"
   ```

2. 创建 skill 符号链接：

   ```bash
   dest="$HOME/.agents/skills/agent-system-prompt-architect"
   mkdir -p "$HOME/.agents/skills"
   if [ -e "$dest" ] || [ -L "$dest" ]; then
     echo "Skill already exists: $dest"
     exit 1
   fi
   ln -s "$repo/skills/agent-system-prompt-architect" "$dest"
   ```

3. 重启 Codex，让它重新发现 skill。

### Windows PowerShell

1. 克隆仓库：

   ```powershell
   $repo = "$env:USERPROFILE\.agents\agent-system-prompt-architect-skill"
   git clone https://github.com/CR-730/agent-system-prompt-architect-skill.git "$repo"
   ```

2. 创建 skills 目录和目录连接：

   ```powershell
   $dest = "$env:USERPROFILE\.agents\skills\agent-system-prompt-architect"
   $source = "$repo\skills\agent-system-prompt-architect"
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   if (Test-Path $dest) {
     Write-Error "Skill already exists: $dest"
     exit 1
   }
   cmd /c mklink /J "$dest" "$source"
   ```

3. 重启 Codex，让它重新发现 skill。

## 仓库级安装（团队共享）

如果只想在某个项目里使用，把 skill 目录复制到该仓库的 `.agents/skills/` 下并提交，Codex 会从当前目录向上扫描到仓库根目录自动发现：

```bash
mkdir -p .agents/skills
cp -r /path/to/agent-system-prompt-architect-skill/skills/agent-system-prompt-architect .agents/skills/
```

## 直接复制安装

如果你不想使用符号链接，也可以直接复制 skill 目录：

```powershell
$dest = "$env:USERPROFILE\.agents\skills\agent-system-prompt-architect"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
if (Test-Path $dest) {
  Write-Error "Skill already exists: $dest"
  exit 1
}
Copy-Item -Recurse -Path .\skills\agent-system-prompt-architect -Destination "$env:USERPROFILE\.agents\skills"
```

这种方式更新时需要重新复制一次。

## 其他平台

本 skill 遵循 [Agent Skills 开放标准](https://agentskills.io/specification)，可直接用于其他兼容平台，只需把 `skills/agent-system-prompt-architect` 目录放到对应平台的 skill 目录，例如：

- Claude Code：`~/.claude/skills/`（个人）或项目内 `.claude/skills/`（团队共享）

## 验证

检查 skill 文件是否存在：

```powershell
Test-Path "$env:USERPROFILE\.agents\skills\agent-system-prompt-architect\SKILL.md"
```

重启 Codex 后，可以在对话中显式调用：

```text
请使用 $agent-system-prompt-architect 帮我设计一个 agent system prompt。
```

## 更新

如果使用符号链接或目录连接：

```bash
cd ~/.agents/agent-system-prompt-architect-skill
git pull
```

Windows PowerShell：

```powershell
cd "$env:USERPROFILE\.agents\agent-system-prompt-architect-skill"
git pull
```

更新后重启 Codex。

## 卸载

macOS / Linux：

```bash
rm ~/.agents/skills/agent-system-prompt-architect
```

Windows PowerShell：

```powershell
cmd /c rmdir "%USERPROFILE%\.agents\skills\agent-system-prompt-architect"
```

可选：删除克隆的仓库目录。
