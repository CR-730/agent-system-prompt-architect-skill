# Evaluation Checklist

## Automatic checks
- The system prompt includes the sections needed for the target agent's role, scope, context, tools, output contract, safety, failure handling, and self-checks
- The main instruction appears before context, examples, and detailed constraints
- All variable slots are either resolved or intentionally preserved
- No direct contradictions across role, scope, tools, and safety rules
- Tool instructions distinguish broad capabilities from real runtime tool specs
- When real tool specs are available, tool contracts include exact names, required inputs, expected output fields, missing-input behavior, post-call checks, conflict handling, and fallback actions
- When real tool specs are unavailable, the prompt asks for the missing specs or states explicit interface assumptions instead of inventing hidden APIs
- Semantic tool capabilities are written as behavior rules, not API-looking contracts with invented names, parameters, return fields, or call policies
- Data retention behavior is specified when the target agent stores, remembers, exports, or modifies user data; missing required retention policy is marked as a product decision the user must define
- If the task is factual, uncertainty and grounding rules are present
- The prompt uses the user's requested or implied language
- Section names, tags, labels, examples, and workflow templates use the user's requested or implied language
- The prompt prefers clear target behavior, output format, decision criteria, and alternative actions over abstract prohibitions
- Repeated rules are consolidated; the same behavior is not restated across multiple sections without adding a new decision criterion
- External source families are defined before grounding rules rely on them
- Common user workflows have compact output templates with section labels and completion criteria
- Domain boundaries include safe alternative actions, especially for academic, legal, medical, financial, privacy, or destructive-action contexts
- The final system prompt is compact enough for deployment: prefer 6 top-level sections, use up to 8 only when justified, and merge overlapping retrieval/tool/failure rules
- Self-check content is short and focused on the highest-risk failures
- Domain-specific rules are grounded in user-provided constraints or explicit assumptions, not hidden guesses
- Ambiguous labels distinguish response language from subject domain; the prompt asks for clarification or states the chosen assumption
- The draft has been compressed once before delivery to remove repeated safety, retrieval, tool, and failure-handling rules
- Semantic tool capabilities are grouped into retrieval/read tools, write/update tools, and planning/generation tools when exact runtime specs are unavailable
- Output templates are compact label lists rather than long per-task policy sections
- Format-sensitive requirements include compact examples or labels; simple requirements stay zero-shot
- Optional prompt techniques are selected only when they improve observable behavior; reasoning-heavy prompts use concise visible summaries rather than full hidden reasoning
- Complex or multi-tool prompts include a compact tool contract covering name, use case, required inputs, optional inputs, returned fields, side effects, confirmation needs, failure handling, and result checks

## Safety checks
- Reasoning visibility is limited to the summary needed for the user-facing task
- Destructive or irreversible actions require confirmation and state the visible result
- Proprietary or hidden prompt content is protected through a safe redirection
- PII collection is limited to task-relevant fields

## Suggested thresholds
- required_section_coverage = 100%
- contradiction_count = 0
- critical_safety_violations = 0
- tool_contract_coverage = 100%
- factual_grounding_pass_rate >= 0.90 for grounded tasks
- style_conformity >= 4/5 on LLM judge

## Review order
1. Required section coverage
2. Safety and privacy
3. Tool contract executability
4. Duplication and priority clarity
5. Length and section economy
6. Output templates and source definitions
7. Domain assumptions and explicit constraints
8. Domain fit and style

## Rollback rule
If a revision lowers any already-passing critical metric, revert to the last passing snapshot before making further edits.
