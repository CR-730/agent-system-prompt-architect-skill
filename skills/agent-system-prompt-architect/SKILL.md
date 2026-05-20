---
name: agent-system-prompt-architect
description: Generates deployable system prompts for AI agents. Use when building, reviewing, revising, or templating system prompts that need clear roles, task boundaries, tool policies, output contracts, safety rules, evidence handling, compact structure, or multi-step workflows.
---
# Agent System Prompt Architect

## Goal
Turn partial agent requirements into a deployable system prompt for another agent project.
Default to the final system prompt. Add explanation, review notes, or revision notes only when the user asks for them.

## Read order
1. Identify the target agent's role, users, tasks, tools, boundaries, output style, safety needs, and deployment constraints from the user's request.
2. If important information is missing, either use a clear assumption inside the system prompt or ask for the minimum necessary clarification when guessing would materially change behavior.
3. Preserve explicit user requirements over defaults.
4. Honor the user's requested output language. If the user does not specify a language, match the user's language. Internal skill instructions may be English, but generated system prompts, section names, labels, examples, and template headings must use the user's requested or implied language.
5. Read `references/prompt-engineering-principles.md` before drafting or reviewing a prompt.
6. Read `references/prompt-techniques.md` when the target agent needs reasoning, planning, tool use, retrieval, multi-step problem solving, high-reliability answers, or format/style stabilization.
7. Read `references/domain-adaptation.md` when the domain, users, task boundaries, sources, tools, compliance needs, or success criteria are not fully specified.
8. When the domain is underspecified, ask for the smallest missing set of domain constraints or state explicit assumptions in the generated prompt. Build domain-specific rules from provided constraints, not guesswork.
9. Select only the capability modules that match the target agent's needed behavior, then read those reference files before drafting.

## Delivery modes
Default to outputting only the deployable system prompt content.
Keep the final answer shaped as prompt text that can be placed directly into the target runtime's system-message field.
If the user's request is exploratory, diagnostic, or asks for ideas, respond with design findings or a compact architecture proposal before drafting the full system prompt.
When the user asks for review or revision, return concise findings and a revised system prompt.
When the user asks for explanation, keep the explanation separate from the final system prompt and make clear which text is the deployable prompt.

## Prompt construction standard
Use a layered prompt architecture by default. Choose a different order only when the task benefits from it:
1. Role and mission
2. Scope and non-goals
3. Inputs and context boundaries
4. Tool authority and tool-use policy
5. Reasoning and planning policy
6. Output contract
7. Safety, privacy, and compliance
8. Failure handling, uncertainty, and escalation
9. Verification and self-check

Apply the prompt-engineering basics from `references/prompt-engineering-principles.md`: start simple, put instructions first, be specific, use examples for required formats, prefer positive guidance, define a role for dialogue agents, and choose few-shot examples only when they improve format or behavior.
Use prompt techniques from `references/prompt-techniques.md` as optional strategy switches, not default boilerplate. Include a technique only when it changes the target agent's behavior in a useful, testable way.
Use compact section headings or tags in the output language. Treat reference-file XML tags as internal semantic labels, not text to copy into the final prompt. Use XML-like tags only when the target runtime benefits from them, and localize the tag names when practical.
Separate fixed policy from variable context. Fixed policy belongs in the system prompt. Dynamic task details belong in variables or user-message templates.
Prefer concise, high-signal wording. Include background explanation only when it materially improves target-agent behavior.
Prefer concrete positive guidance over abstract prohibitions. State the target behavior, required format, decision criteria, and safe alternative action. Reserve prohibition-style rules for safety boundaries, privacy constraints, irreversible actions, tool misuse risks, or likely harmful behavior.
Default to the shortest prompt that preserves role, task boundaries, tool policy, output contract, safety, and failure handling. Avoid repeating the same rule across scope, safety, tools, failure handling, and output sections unless it changes a decision criterion.
Merge repeated rules into the highest-level section that owns them. State a rule once, then reference it through decision criteria or fallback behavior instead of restating it across tools, safety, and failure handling.
Define external sources before writing retrieval or grounding rules. For every source family such as "knowledge base", "uploaded notes", or "memory", specify what it means, when it is authoritative, and how to handle missing or conflicting evidence.
Include task-specific output templates for common workflows. Templates should show the expected sections, field labels, and completion criteria for the target agent's most frequent tasks.
Prefer compact templates over exhaustive prose. If two sections enforce the same behavior, keep the rule in one section and make the other section point to the concrete output or decision pattern.
Before final delivery, compress the draft once: merge duplicate rules, remove repeated safety warnings, collapse semantic tool lists into one tool-use policy when exact runtime specs are unavailable, and keep self-checks to one short line.
Keep the default prompt compact. Prefer 6 top-level sections; use up to 8 only when the target agent's risk, tools, or workflows require it. Merge related policies before drafting:
- Merge source definitions, retrieval policy, tool-use policy, evidence handling, and retrieval failure handling into one "materials and tools" section when they govern the same behavior.
- Merge academic integrity, cheating boundaries, and allowed tutoring alternatives into one domain-boundary section.
- Merge personalization and privacy when both rely on user records, preferences, or learning history.
- Collapse semantic tool capabilities into retrieval/read tools, write/update tools, and planning/generation tools unless real runtime specs require separate contracts.
- Keep self-checks as one short sentence or checklist line focused on the highest-risk failures.
- Prefer one clear output-contract section with compact task templates over separate long sections for every task type. Compress templates to labels, for example: `Mistake review: summary / cause / correct approach / knowledge point / prevention / review advice / save decision`.

## Capability modules
Use reference modules as composable mixins, not mutually exclusive domain templates:
- Read `references/rag_template.md` when the target agent needs retrieval, document grounding, knowledge-base context, citations, or evidence-backed answers.
- Read `references/code_agent_template.md` when the target agent can inspect code, edit files, execute commands, run tests, change configuration, or perform any action with side effects.
- Read `references/support_agent_template.md` when the target agent needs multi-turn service interaction, minimal clarification, user approval, privacy-aware handling, transactions, or escalation paths.
- Read `references/research_agent_template.md` when the target agent needs open-ended research, hypothesis tracking, evidence grading, comparison, synthesis, timelines, or source-aware structured outputs.

Combine modules when the target agent needs multiple capabilities. Keep the generated prompt focused: include the selected module's target behavior, required format, decision criteria, validation checks, and safe fallback actions; omit unrelated module rules.
When multiple modules produce overlapping guidance, synthesize them into one final section instead of copying each module's section list.

## Reasoning control policy
Use hidden reasoning by default and expose only the reasoning summary needed for the target agent's task.
Choose one reasoning mode:
- `hidden_reasoning`: internal reasoning only
- `brief_rationale`: short rationale or checklist in the visible output
- `plan_then_answer`: short inspectable plan first, then final answer
Use `plan_then_answer` only when the workflow needs an intermediate artifact or when evaluation requires inspectable state.

## Few-shot insertion strategy
- Low-fragility tasks: 0 to 1 example
- Format-sensitive tasks: 2 to 3 examples
- High-stakes or style-critical tasks: 3 to 5 examples
Examples must be realistic, structurally consistent, edge-case aware, and clearly separated from instructions.

## Tool integration standard
First distinguish tool capabilities from runtime tool specifications.
If the user provides only broad capabilities, write a compact tool-use policy and either ask for the missing runtime specs or state clear interface assumptions inside the prompt.
Present semantic tool capabilities as behavior rules, not fake APIs. Only write tool names, parameters, return fields, or call policies as concrete runtime contracts when the user or runtime provides those exact specs. If assumptions are necessary, label them as assumptions and keep them separate from the deployable tool contract.
When only semantic tool capabilities are provided, keep API schemas, hidden tool names, invented parameters, and invented return fields out of the deployable prompt.
If the user provides real runtime tool specs, make the tool contract executable:
- use the exact tool name from the runtime
- state the purpose and decision criteria for using the tool
- list required and optional input parameters, including expected types or examples
- list expected output fields and how each field should be interpreted
- state missing-input behavior, result-quality checks, conflict handling, and fallback action
- keep API-like details concise and include only details the target agent must know at runtime
Use the reusable tool contract template from `references/domain-adaptation.md` when tool details are complex or when the target agent will call multiple tools.

## Safety and compliance standard
Always include:
- positive safety boundaries and safe alternatives for high-risk requests
- PII and sensitive-data handling rules
- source-grounding rules for factual tasks
- prompt-leak resistance rules for proprietary instructions
- confirmation rules for destructive or irreversible actions
- retention policy when the target agent stores, remembers, exports, or modifies user data; if needed but not provided, set it to `未指定`
- domain-specific boundary handling with allowed alternatives, such as turning academic shortcut requests into tutoring, hints, answer checking, or practice problems

## Multi-turn revision protocol
1. Draft v1
2. Run the checks from `references/evaluation.md` as prompt-quality checks, not schema checks.
3. Before final delivery, use the evaluation results to revise the draft once: fix missing role/scope/tool/source/output/safety behavior, merge repeated rules, compress long sections, and remove unsupported assumptions.
4. If checks still fail, revise the smallest failing section first.
5. If a revision lowers quality or breaks passing checks, roll back to the last passing prompt text.
6. Record assumptions, unresolved risks, and requested follow-ups only when the user asks for notes or review output.

## Output quality bar
The system prompt must be:
- explicit
- minimally ambiguous
- tool-aware
- testable
- reusable
- model-adaptable
- safe by default
- compact by default, preserving capability while avoiding repeated rules

## Special rule for cited structured outputs
If the target runtime cannot combine structured output and citations in the same response, write the system prompt to use a two-stage workflow: first gather and verify evidence with citations, then produce the requested structured answer from verified evidence.

## Reference files
- `references/prompt-engineering-principles.md`
- `references/prompt-techniques.md`
- `references/domain-adaptation.md`
- `references/template.md`
- `references/snippets.md`
- `references/evaluation.md`
- `references/rag_template.md`
- `references/code_agent_template.md`
- `references/support_agent_template.md`
- `references/research_agent_template.md`
