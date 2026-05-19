# Agent System Prompt Architect Skill

A Codex/Agent Skill for generating deployable system prompts for AI agents.

This skill focuses on direct system-message output: compact, tool-aware, source-aware, and safe-by-default prompts that can be placed into an agent runtime. It avoids JSON/package wrappers by default and uses references only as composable guidance.

## What It Helps With

- Designing system prompts for new agents
- Reviewing and revising existing prompts
- Separating broad tool capabilities from real runtime tool specs
- Handling domain ambiguity without guessing hidden rules
- Keeping final prompts compact, usually around 6 top-level sections
- Writing prompt rules with clear target behavior, formats, decision criteria, and fallback actions

## Repository Layout

```text
agent-system-prompt-architect-skill/
├── README.md
├── LICENSE
└── skills/
    └── agent-system-prompt-architect/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── domain-adaptation.md
            ├── evaluation.md
            ├── rag_template.md
            ├── code_agent_template.md
            ├── support_agent_template.md
            ├── research_agent_template.md
            ├── snippets.md
            └── template.md
```

## Installation

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\agent-system-prompt-architect "$env:USERPROFILE\.codex\skills\agent-system-prompt-architect"
```

Or for Claude Code-style layouts, copy the same folder into your skills directory:

```bash
cp -r skills/agent-system-prompt-architect ~/.claude/skills/agent-system-prompt-architect
```

Restart or reload your agent runtime after installation if required.

## Example Usage

```text
Use $agent-system-prompt-architect to create a deployable system prompt for a customer support agent.
```

For exploratory requests, the skill should first return a compact architecture proposal. For direct build requests, it should return system prompt text that can be placed into the target runtime's system-message field.

## Design Notes

The skill uses capability modules rather than vertical domain templates:

- `domain-adaptation.md`: domain questions, ambiguity handling, and reusable tool contract template
- `rag_template.md`: retrieval, grounding, sources, and citations
- `code_agent_template.md`: execution, side effects, verification, and rollback
- `support_agent_template.md`: multi-turn service flow, privacy, approvals, and escalation
- `research_agent_template.md`: evidence grading, synthesis, and uncertainty handling

The final prompt is expected to synthesize these modules, not copy every module section verbatim.

## License

MIT
