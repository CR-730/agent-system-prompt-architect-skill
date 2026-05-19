# RAG Template Module

This file is a composable capability module, not a standalone agent category.
The XML tag names are semantic placeholders. In the final system prompt, translate section names and labels into the user's requested or implied language.

## Purpose
Use this module when the target agent depends on retrieval results, knowledge-base hits, document chunks, policy excerpts, FAQ entries, citations, or other approved external context.

The module's goal is context grounding: the generated prompt should tell the agent how to identify usable evidence, format evidence-backed answers, decide when context is insufficient, and choose a safe next action.

## Sections to add
- `<source_definitions>`
- `<knowledge_boundary>`
- `<retrieval_policy>`
- `<citation_policy>`
- `<context_fallback>`
- `<conflict_resolution>`

## Prompt fragment
```xml
<source_definitions>
Define each source family the agent may rely on: user message, uploaded files, knowledge base, memory, tool result, and general model knowledge.
For each source, specify when it is authoritative, how to label it in answers, and what to do when it is missing or conflicts with another source.
</source_definitions>

<knowledge_boundary>
Treat approved retrieved context as the factual basis for grounded answers.
Separate retrieved evidence, user-provided facts, and model inference.
If the context does not cover the question, state the evidence gap and request the smallest useful retrieval or clarification.
</knowledge_boundary>

<retrieval_policy>
Retrieve before answering when the task depends on fresh, private, policy-specific, or document-specific facts.
Prefer relevant, recent, authoritative, and directly quoted evidence.
Use the retrieved context to answer the user's concrete question instead of summarizing all retrieved material.
</retrieval_policy>

<citation_policy>
Attach source labels, document names, record ids, or citation markers to important factual claims when the runtime supports it.
When structured output and citations cannot be produced in the same response, first produce an evidence record with sources, then produce the requested structured answer from verified facts.
</citation_policy>

<context_fallback>
When retrieval returns weak or no evidence, say what is known, what is missing, and what exact query, document, or user clarification would resolve the gap.
</context_fallback>

<conflict_resolution>
When sources conflict, preserve the conflict, identify which source supports each claim, and state the decision rule for the next step.
</conflict_resolution>
```

## Example input
```yaml
question: Does the refund policy allow returns within 7 days after delivery?
retrieved_context:
  - title: Help Center Refund Policy
    excerpt: Non-customized goods may be returned within 7 days after delivery.
  - title: Promotion Terms
    excerpt: Some sale items are excluded from no-reason returns.
```

## Example output behavior
```yaml
answer: Standard policy allows returns within 7 days after delivery, but sale-item exclusions may apply.
evidence_status: confirmed_with_exception
next_action: Check whether the item belongs to an excluded promotion category.
```

## Tool policy example
```yaml
tool: search_kb
input:
  query: refund policy sale item exclusion 7 days delivery
  top_k: 5
```

## Evaluation focus
- source_coverage
- quote_or_excerpt_support_rate
- unsupported_claim_count
- contradiction_retention_rate
- retrieval_precision_on_key_queries
