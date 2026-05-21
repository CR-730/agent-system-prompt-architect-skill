# Prompt Engineering Principles

This reference captures the basic prompt-writing principles used by this skill, adapted from common prompt-engineering guidance.

Use these principles as a writing and review checklist. Keep the final deployable prompt compact.

## Core Elements
A useful prompt usually combines only the elements needed for the task:

- Instruction: what the agent should do
- Context: source material, background, constraints, and operating conditions
- Input data: what the user or runtime provides
- Output indicator: format, style, sections, or completion criteria

Do not force all four elements into every prompt. Simple tasks can stay simple.

## Basic Rules

1. Start simple.
   - Begin with the shortest prompt that can preserve role, task, boundaries, output format, and safety.
   - Add detail only when it improves behavior, reduces ambiguity, or covers a real risk.

2. Put instructions first.
   - Lead with the agent's role, mission, and main task.
   - Put context and examples after the main instruction.

3. Be specific and measurable.
   - Prefer concrete counts, formats, labels, decision criteria, and completion standards.
   - Replace vague wording such as "not too much" with concrete wording such as "3 to 5 bullet points".
   - State stable facts and decision criteria; avoid turning heuristics into fixed execution paths.

4. Use examples to clarify formats.
   - Add examples when output shape matters, when labels are easy to confuse, or when the target runtime needs consistent structure.
   - Keep examples short and representative.

5. Prefer positive guidance.
   - State what the agent should do, how it should respond, and what safe alternative to use.
   - Use prohibition-style wording mainly for safety, privacy, irreversible actions, tool misuse, and high-risk boundary cases.
   - Use fewer abstract prohibitions and more concrete goals, required formats, decision criteria, and alternative behaviors. For example, prefer "When evidence is missing, state the gap and ask for the exact missing source" over a broad warning such as "Do not hallucinate."

6. Define roles for dialogue agents.
   - Specify who the agent is helping, what role it plays, and what tone or interaction pattern fits the task.

7. Use few-shot examples selectively.
   - Default to zero-shot for straightforward prompts.
   - Add 1 to 3 examples for format-sensitive, style-sensitive, or easily confused behaviors.
   - Avoid long example blocks that crowd out the actual instruction.

8. Decompose complex tasks.
   - Split broad workflows into short stages or task templates.
   - Use workflow templates only for high-frequency tasks.

9. Favor procedures over declarations.
   - Write a reusable method the agent can apply across cases, not a fixed answer for one case.
   - Example, weak (declaration): "Join `orders` to `customers` on `customer_id`, filter `region='EMEA'`, sum `amount`." Useful only for that one query.
   - Example, strong (procedure): "Identify the entities the user is asking about. Join the relevant tables on the matching id. Apply user-specified filters as conditions. Aggregate the requested numeric column. Return the result as a labeled table."
   - Treat names from the user's example as request shape, not as fixed schema. Table names, field names, filter values, regions, dates, and metric names are illustrations of what the agent might receive, not defaults it must use. Bake them into the prompt as fixed values only when the user explicitly says they are real runtime facts.
   - Procedures generalize; one-off declarations bake the wrong abstraction into the prompt.

10. Match specificity to task fragility.
    - High-freedom wording for tasks where multiple paths are valid and judgment matters.
    - Low-freedom wording (exact commands, ordered steps, fixed templates) only where mistakes are costly, ordering matters, or the runtime is fragile.
    - When an open-ended task still benefits from a default sequence, frame it as a default flow with explicit permission to adapt (e.g., "Apply this sequence unless the input calls for a different order"), not as mandatory steps.
    - Over-specifying a flexible task narrows the agent's judgment without improving outcomes.

11. Provide defaults, not menus.
    - When several options are technically valid, name one default and give an escape hatch for the known exception.
    - Example, weak: "You can use library A, B, C, or D depending on context."
    - Example, strong: "Use library A. If the input is X, use library B instead."
    - Listing many equally-weighted choices makes the agent stall or pick inconsistently.

## Add only what the agent lacks
Assume the model already understands common tools, file formats, programming concepts, and standard tasks. Spend tokens on:
- project-specific facts the model could not know (codebase conventions, gotchas, names that mean different things in different services)
- decisions the model would otherwise have to guess (which library to default to, which schema is authoritative, what success looks like)
- failure cases the model would not anticipate without hints
Do not spend tokens explaining what something is when the model already knows.

## Review Questions

- Is the instruction at the beginning?
- Are the task, users, and boundaries specific enough?
- Is the output format shown with compact labels or examples?
- Are prohibitions paired with the target behavior or a safe alternative?
- Are prescribed steps reusable methods rather than one-off answers?
- Does the level of specificity match the task's fragility, not exceed it?
- Where multiple valid options exist, is one named as the default?
- Does every section change behavior, or can it be merged or removed?
