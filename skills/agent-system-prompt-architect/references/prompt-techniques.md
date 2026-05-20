# Prompt Techniques

Use this reference when the target agent needs reasoning, planning, retrieval, tools, multi-step problem solving, high reliability, or stable output format/style.

Treat these as optional strategy switches. Add only the techniques that materially improve the target agent's behavior.

| Technique | Use When | How To Express In A System Prompt | Cautions |
|---|---|---|---|
| Zero-shot | The task is straightforward and the desired behavior is clear | Give role, task, boundaries, and output format directly | Keep it short; add examples only after a real need appears |
| Few-shot | Output format, tone, labels, or edge-case behavior is easy to misunderstand | Include 1 to 3 compact examples showing input and desired output shape | Keep examples representative; long examples crowd out the instruction |
| Chain-of-thought style reasoning | The agent must solve multi-step reasoning problems | Use internal reasoning, then expose only a concise solution path, checklist, or rationale needed by the user | Do not request full hidden reasoning in the visible answer |
| Zero-shot-CoT | A simple reasoning task benefits from decomposition | Tell the agent to break the problem into steps before answering, then return the answer in the requested format | Use compact visible steps; avoid verbose reasoning dumps |
| Self-consistency | The answer must be robust and mistakes are costly | Tell the agent to compare multiple candidate approaches internally and return the most reliable answer with a short confidence or check summary | Higher cost and latency; use for high-value decisions, not everyday answers |
| Tree of Thoughts | Planning or decision tasks need multiple candidate paths | Tell the agent to generate candidate plans, score them against criteria, and proceed with the best plan | Heavyweight; keep candidate count small and criteria explicit |
| Step-back prompting | The task benefits from abstraction before solving | Tell the agent to identify the general principle or pattern, then apply it to the current case | Good for teaching, research, strategy, and debugging; keep the principle short |
| ReAct-style tool use | The agent has tools and must decide when to use them | Tell the agent to inspect the request, choose a tool when it improves correctness, check tool results, and then answer | Do not expose internal action traces unless the runtime or user needs them |
| RAG / retrieval grounding | The task depends on external documents, knowledge bases, user files, or fresh facts | Tell the agent to retrieve relevant sources, distinguish evidence from inference, cite or label sources, and handle missing evidence explicitly | Avoid invented sources; define source families and conflict rules |

## Selection Rules

- Default to zero-shot plus clear instructions for simple tasks.
- Add few-shot examples for format-sensitive behavior.
- Use internal reasoning with concise visible summaries for reasoning-heavy tasks.
- Use step-back for teaching, research, debugging, planning, and abstract concepts.
- Use ReAct-style rules only when tools exist.
- Use RAG rules only when external sources or private documents matter.
- Use self-consistency or Tree of Thoughts only for high-risk or high-value tasks where extra latency is acceptable.

## Review Questions

- Which technique is actually needed for this target agent?
- Does the technique add observable behavior, or just extra wording?
- Can the technique be expressed as a short decision rule or output pattern?
- Does the technique increase cost, latency, or verbosity beyond the task's needs?
