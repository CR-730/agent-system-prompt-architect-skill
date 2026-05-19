# Research Agent Template Module

This file is a composable capability module, not a standalone agent category.
The XML tag names are semantic placeholders. In the final system prompt, translate section names and labels into the user's requested or implied language.

## Purpose
Use this module when the target agent performs open-ended search, source comparison, hypothesis tracking, evidence grading, trend synthesis, timelines, research notes, or source-aware structured outputs.

The module's goal is evidence synthesis: the generated prompt should define how to form questions, collect evidence, grade claims, preserve uncertainty, and deliver conclusions in a format that can be audited.

## Sections to add
- `<research_questions>`
- `<hypothesis_management>`
- `<evidence_grading>`
- `<synthesis_policy>`
- `<uncertainty_policy>`
- `<deliverable_modes>`

## Prompt fragment
```xml
<research_questions>
Start by turning the user's objective into specific research questions, evidence needs, and success criteria.
Keep the research scope narrow enough to finish, or explicitly split it into phases.
</research_questions>

<hypothesis_management>
For complex questions, maintain competing hypotheses and track what evidence supports, weakens, or leaves each hypothesis unresolved.
Do not collapse to a single conclusion before the evidence supports it.
</hypothesis_management>

<evidence_grading>
Label important claims as confirmed, inferred, or unknown.
Use multiple sources for high-value factual claims when available. Preserve source conflicts and identify the claim each source supports.
</evidence_grading>

<synthesis_policy>
Build an evidence table or research notes before writing the final synthesis.
Ensure every major conclusion can be traced back to evidence or clearly marked as inference.
</synthesis_policy>

<uncertainty_policy>
Keep unknowns visible. State what evidence would change the conclusion or resolve the uncertainty.
</uncertainty_policy>

<deliverable_modes>
Choose the output form that matches the task: evidence table, executive summary, timeline, comparison matrix, decision memo, or another structured format requested by the user.
When citations and structured output conflict at runtime, deliver evidence with sources first, then produce the requested structured answer from verified results.
</deliverable_modes>
```

## Example input
```yaml
research_question: Did the target company accelerate AI product releases over the last 12 months?
required_outputs:
  - evidence_table
  - executive_summary
  - structured_json
```

## Example output behavior
```yaml
fact: The company publicly released four AI feature updates in the last 12 months.
fact_status: confirmed
inference: The release cadence appears higher than the previous period.
inference_status: inferred
unknown: Internal roadmap and unreleased product plans.
```

## Tool policy example
```yaml
tool_sequence:
  - web_search: target company AI release notes last 12 months
  - web_fetch: selected release pages
  - code_execution: build timeline and compare intervals
```

## Evaluation focus
- claim_support_rate
- source_diversity_score
- fact_inference_unknown_separation
- contradiction_retention_rate
- structured_output_completeness
