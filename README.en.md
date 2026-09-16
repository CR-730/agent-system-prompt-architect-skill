# Agent System Prompt Architect Skill

[中文](README.md) | **English**

[![License: MIT](https://img.shields.io/github/license/CR-730/agent-system-prompt-architect-skill)](LICENSE)
[![Release](https://img.shields.io/github/v/release/CR-730/agent-system-prompt-architect-skill?label=release)](https://github.com/CR-730/agent-system-prompt-architect-skill/releases)
[![Skill](https://img.shields.io/badge/Codex-Skill-blue)](skills/agent-system-prompt-architect/SKILL.md)
[![Standard](https://img.shields.io/badge/Agent%20Skills-spec-brightgreen)](https://agentskills.io/specification)
[![Docs](https://img.shields.io/badge/docs-English-brightgreen)](README.en.md)

A skill that teaches Codex / code agents to write high-quality system prompts for agent projects.

I built it after repeatedly running into malformed system prompts while using Codex on agent projects, and drew on a set of reference materials to put the rules together.

## Contents

- [When to use it](#when-to-use-it)
- [What it fixes](#what-it-fixes)
- [Core capabilities](#core-capabilities)
- [Installation](#installation)
- [Usage examples](#usage-examples)
- [Repository structure](#repository-structure)
- [Design notes](#design-notes)
- [References](#references)

## When to use it

Use this skill when you want an agent to write the system prompt for another agent.

Not a good fit:

- You just want a one-off casual prompt
- The target is not an agent system prompt, but marketing copy, an article, a script, or an ordinary chat prompt

## What it fixes

Common failure modes when an agent writes a system prompt:

- Using a project, brand, or codename as the role name (e.g. "You are the Xiaohongshu agent")
- Copying backend code identifiers straight into the system prompt
- Piling up "don't do this" rules with no clear specification or constraints
- Inventing tool names, parameters, and return fields when no real tool definitions exist
- Writing a very long system prompt with no layered structure

## Core capabilities

- Produces system prompts that can be dropped into an agent as-is
- Designs clear roles, task scope, non-goals, and failure handling
- Reduces hallucinated output
- Separates semantic tool capabilities from real runtime tool specs
- Handles sources, retrieval, citations, evidence conflicts, and uncertainty
- Applies standard prompt-engineering principles: specific instructions, positive guidance, format examples, measurable success criteria
- Selects advanced prompt techniques on demand: few-shot, reasoning policy, ReAct-style tool use, retrieval grounding
- Runs an internal check against `references/evaluation.md` after the first draft, then compresses and revises

## Installation

Installation via [.codex/INSTALL.md](.codex/INSTALL.md) is recommended — it covers clone, link, verification, update, and uninstall on macOS / Linux / Windows, plus repo-level installation (`.agents/skills/`) and other platforms such as Claude Code.

Quick copy install (user level, current Codex convention path):

```powershell
$dest = "$env:USERPROFILE\.agents\skills\agent-system-prompt-architect"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
if (Test-Path $dest) {
  Write-Error "Skill already exists: $dest"
  exit 1
}
Copy-Item -Recurse -Path .\skills\agent-system-prompt-architect -Destination "$env:USERPROFILE\.agents\skills"
```

> Older Codex versions use `~/.codex/skills`. If yours is older, replace `.agents` with `.codex` in the command above.

Restart Codex after installation so it rediscovers the skill.

## Usage examples

```text
Use $agent-system-prompt-architect

I want to build a study assistant agent for high-school and early-college students.
It needs to explain course concepts, answer questions from user-uploaded material,
organize wrong answers, and build revision plans.
The system may expose tools for retrieving user material, searching a course knowledge
base, saving wrong answers, and generating study plans, but I have not settled on the
real tool names, parameters, or return formats yet.

Write me a system prompt I can put straight into the system message.
```

If you are still exploring the idea:

```text
Use $agent-system-prompt-architect

I want to build a Q&A agent for an enterprise knowledge base.
First tell me which modules its system prompt should contain — don't rush into
writing the full prompt.
```

## Repository structure

```text
agent-system-prompt-architect-skill/
├── .codex/
│   └── INSTALL.md
├── skills/
│   └── agent-system-prompt-architect/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── references/
│           ├── prompt-engineering-principles.md
│           ├── prompt-techniques.md
│           ├── domain-adaptation.md
│           ├── evaluation.md
│           ├── rag_template.md
│           ├── code_agent_template.md
│           ├── support_agent_template.md
│           ├── research_agent_template.md
│           ├── snippets.md
│           └── template.md
├── RELEASE-NOTES.md
├── README.en.md
└── README.md
```

## Design notes

1. Splits standard prompt-engineering rules and advanced techniques into separate reference files, so the agent writes against the baseline pattern first and then selects few-shot, reasoning strategy, ReAct-style tool use, or retrieval grounding as the scenario requires.
2. After the first draft, runs an internal quality check against the evaluation checklist, then compresses, merges duplicate rules, and removes anything that is not deployable.
3. Adds a domain-adaptation checklist so the agent adapts to the target users, task, sources, tool side effects, output format, and safety boundaries.
4. Translates concrete code identifiers into agent-executable behavior rules.
5. Ships standard templates for several agent capabilities: retrieval-augmented, code-execution, customer-support, and research scenarios.

## References

- [Agent Skills open standard](https://agentskills.io/specification)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [Prompt Engineering Notes](https://www.aneasystone.com/archives/2024/01/prompt-engineering-notes.html)

## License

MIT
