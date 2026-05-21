感谢佬的 star，初来乍到可能很多地方不规范，有问题或者建议希望可以在 issues 跟我提，我会马上跟进! 

起因是本人用 codex 写 agent 项目时总是遇到它给 agent 写的提示词一言难尽的问题，并且没有找到其他佬开源的类似的 skill，因此结合一些资料创建了一个让它学会怎么写提示词的 skill 。

# Agent System Prompt Architect Skill

A Codex/Agent Skill for generating deployable system prompts for AI agents.

This skill helps a code agent design strong system prompts for agent projects, covering role definition, task boundaries, tool-use rules, evidence handling, output formats, and safety behavior.

## What It Helps With

- Designing system prompts for new agents
- Reviewing and revising existing prompts
- Separating broad tool capabilities from real runtime tool specs
- Handling domain ambiguity without guessing hidden rules
- Keeping final prompts compact, usually around 6 top-level sections
- Writing prompt rules with clear target behavior, formats, decision criteria, and fallback actions
- Applying prompt-engineering standards such as specific instructions, positive guidance, format examples, and measurable success criteria
- Choosing advanced prompting techniques only when useful, such as few-shot examples, reasoning policies, ReAct-style tool use, or retrieval grounding

## Repository Layout

```text
agent-system-prompt-architect-skill/
├── README.md
├── LICENSE
├── scripts/
│   └── run_skill_evals.py
├── test/
│   ├── evals.json
│   ├── triggers.json
│   └── README.md
└── skills/
    └── agent-system-prompt-architect/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── domain-adaptation.md
            ├── evaluation.md
            ├── prompt-engineering-principles.md
            ├── prompt-techniques.md
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


- `domain-adaptation.md`: domain questions, ambiguity handling, and reusable tool contract template
- `prompt-engineering-principles.md`: baseline prompt-writing standards, including concrete goals, required formats, decision criteria, positive guidance, and safe alternatives
- `prompt-techniques.md`: when to use advanced techniques such as few-shot examples, reasoning policies, ReAct-style tool use, step-back prompting, or retrieval grounding
- `rag_template.md`: retrieval, grounding, sources, and citations
- `code_agent_template.md`: execution, side effects, verification, and rollback
- `support_agent_template.md`: multi-turn service flow, privacy, approvals, and escalation
- `research_agent_template.md`: evidence grading, synthesis, and uncertainty handling

The final prompt is expected to synthesize these modules.


## License

MIT
