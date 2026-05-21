# Domain Adaptation

Use this reference to adapt a system prompt to a domain without creating vertical domain-specific templates.

## Domain Adaptation Checklist
Answer these questions from the user's request before drafting. If an answer is missing and materially changes behavior, ask the smallest necessary clarification or state the assumption explicitly in the generated prompt.

1. Who are the target users?
2. What high-frequency tasks should the agent complete?
3. Which tasks are outside the agent's role or require a safer alternative?
4. Which information sources should the agent rely on?
5. Are tools available, and do any tools have side effects?
6. Does the agent need citations, evidence, audit records, or traceable decisions?
7. Does the output need a fixed format or task-specific templates?
8. Which safety, compliance, privacy, or integrity boundaries apply?
9. Which situations require user confirmation, refusal, fallback, or escalation?
10. What makes an output successful for this domain?

Clarification priority: ask at most 3 questions first. Prefer this order:
1. One concrete sample input plus the desired output for the most common task. A real example resolves more ambiguity than any number of checklist answers.
2. Hard boundaries (privacy, safety, irreversible actions) that change which behaviors are allowed.
3. Tools the agent may call and their side effects.
4. Target users and the highest-frequency tasks, if not already revealed by the sample.

Resolve only gaps that would change the generated agent's behavior, safety boundary, tool use, source grounding, or output format. Do not fill every checklist item.
When a domain label is ambiguous, distinguish response language from subject domain. For example, "Chinese learning assistant" may mean an assistant that answers in Chinese or an assistant for Chinese-language/literature coursework. If unclear, ask one minimal clarification or state the assumption explicitly.
Treat names as labels, not roles; derive roles from tasks, users, responsibilities, and success criteria, and ask one clarification when the name is the only clue.

## Tool Contract Template
Use this template when the user provides real runtime tool specs or when multiple tools need consistent treatment. Keep it compact in the final system prompt.

- Tool name:
- Use case:
- Required inputs:
- Optional inputs:
- Returned fields:
- Side effects:
- User confirmation needed:
- Failure handling:
- Result checks:

## Adaptation Rules
- Keep this as a checklist, not a domain knowledge base.
- Derive domain rules from user-provided constraints, source descriptions, tool specs, and success criteria.
- Prefer explicit assumptions over hidden domain guesses.
- Use output templates for high-frequency tasks instead of adding long domain background.
- For deployable prompts, prefer a compact shape; group sections by shared decision criteria rather than by a fixed template.
