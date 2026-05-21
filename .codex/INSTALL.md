# 为 Codex 安装 Agent System Prompt Architect Skill

通过 Codex 原生 skill 发现机制安装本仓库的 `agent-system-prompt-architect` skill。推荐使用符号链接或 Windows 目录连接，这样后续 `git pull` 后可以即时更新。

## 前置条件

- Git
- Codex 已安装并能读取用户目录下的 skills

## 安装步骤

### macOS / Linux

1. 克隆仓库：

   ```bash
   repo="$HOME/.codex/agent-system-prompt-architect-skill"
   git clone https://github.com/CR-730/agent-system-prompt-architect-skill.git "$repo"
   ```

2. 创建 skill 符号链接：

   ```bash
   dest="$HOME/.codex/skills/agent-system-prompt-architect"
   mkdir -p "$HOME/.codex/skills"
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
   $repo = "$env:USERPROFILE\.codex\agent-system-prompt-architect-skill"
   git clone https://github.com/CR-730/agent-system-prompt-architect-skill.git "$repo"
   ```

2. 创建 skills 目录和目录连接：

   ```powershell
   $dest = "$env:USERPROFILE\.codex\skills\agent-system-prompt-architect"
   $source = "$repo\skills\agent-system-prompt-architect"
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills"
   if (Test-Path $dest) {
     Write-Error "Skill already exists: $dest"
     exit 1
   }
   cmd /c mklink /J "$dest" "$source"
   ```

3. 重启 Codex，让它重新发现 skill。

## 直接复制安装

如果你不想使用符号链接，也可以直接复制 skill 目录：

```powershell
$dest = "$env:USERPROFILE\.codex\skills\agent-system-prompt-architect"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills"
if (Test-Path $dest) {
  Write-Error "Skill already exists: $dest"
  exit 1
}
Copy-Item -Recurse -Path .\skills\agent-system-prompt-architect -Destination "$env:USERPROFILE\.codex\skills"
```

这种方式更新时需要重新复制一次。

## 验证

检查 skill 文件是否存在：

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\agent-system-prompt-architect\SKILL.md"
```

重启 Codex 后，可以在对话中显式调用：

```text
请使用 $agent-system-prompt-architect 帮我设计一个 agent system prompt。
```

## 更新

如果使用符号链接或目录连接：

```bash
cd ~/.codex/agent-system-prompt-architect-skill
git pull
```

Windows PowerShell：

```powershell
cd "$env:USERPROFILE\.codex\agent-system-prompt-architect-skill"
git pull
```

更新后重启 Codex。

## 卸载

macOS / Linux：

```bash
rm ~/.codex/skills/agent-system-prompt-architect
```

Windows PowerShell：

```powershell
cmd /c rmdir "%USERPROFILE%\.codex\skills\agent-system-prompt-architect"
```

可选：删除克隆的仓库目录。
