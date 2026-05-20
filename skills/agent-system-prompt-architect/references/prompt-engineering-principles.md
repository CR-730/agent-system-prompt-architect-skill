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

4. Use examples to clarify formats.
   - Add examples when output shape matters, when labels are easy to confuse, or when the target runtime needs consistent structure.
   - Keep examples short and representative.

5. Prefer positive guidance.
   - State what the agent should do, how it should respond, and what safe alternative to use.
   - Use prohibition-style wording mainly for safety, privacy, irreversible actions, tool misuse, and high-risk boundary cases.

6. Define roles for dialogue agents.
   - Specify who the agent is helping, what role it plays, and what tone or interaction pattern fits the task.

7. Use few-shot examples selectively.
   - Default to zero-shot for straightforward prompts.
   - Add 1 to 3 examples for format-sensitive, style-sensitive, or easily confused behaviors.
   - Avoid long example blocks that crowd out the actual instruction.

8. Decompose complex tasks.
   - Split broad workflows into short stages or task templates.
   - Use workflow templates only for high-frequency tasks.

## Review Questions

- Is the instruction at the beginning?
- Are the task, users, and boundaries specific enough?
- Is the output format shown with compact labels or examples?
- Are repeated warnings replaced by target behavior and safe alternatives?
- Does every section change behavior, or can it be merged or removed?
