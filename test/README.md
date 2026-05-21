# Evals for `agent-system-prompt-architect`

These evals exist for two questions, kept separate so they can be optimized independently:

1. **Triggering** — does the skill's frontmatter `description` cause Claude (or another agent harness) to pick this skill on the right requests and skip it on the wrong ones?
2. **Output quality** — when the skill is selected, does the deployable system prompt it produces meet the quality bar in `references/evaluation.md`?

The structure follows [agentskills.io / evaluating-skills](https://agentskills.io/skill-creation/evaluating-skills) and [agentskills.io / optimizing-descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

## Files

- `evals.json` — output-quality test cases. Each case targets a specific failure mode this skill is built to prevent (runtime artifact leakage, pipeline-step roles, declaration baked into rules, etc.).
- `triggers.json` — should-trigger and should-not-trigger queries split into train (60%) and validation (40%) sets, used only when tuning the description.

## Automated runner

The repository includes `scripts/run_skill_evals.py`, which runs both output-quality and trigger evals against an OpenAI-compatible chat endpoint. The default model is `mimo-v2.5-pro`.

Set credentials in the shell or in a local `.env` file (gitignored):

```powershell
$env:MIMO_API_KEY="..."
$env:MIMO_BASE_URL="https://token-plan-cn.xiaomimimo.com/v1"
$env:MIMO_MODEL="mimo-v2.5-pro"
```

Install dependencies and run a smoke pass:

```powershell
uv sync
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --limit 1 --iteration smoke-001
```

Run the full benchmark:

```powershell
uv run python scripts\run_skill_evals.py --quality --triggers --with-baseline --iteration full-001
```

Run a single case (repeat `--case` for several):

```powershell
uv run python scripts\run_skill_evals.py --quality --case abstract-minimal-input --iteration ad-hoc-001
```

Results are written under `evals-workspace/<iteration>/`, with per-case outputs, timing, grading evidence, trigger decisions, and `benchmark.json`.

## Workspace layout for runs

Keep generated artifacts outside the skill directory so the skill itself stays small. Recommended layout:

```
agent-system-prompt-architect-skill/
├── skills/
│   └── agent-system-prompt-architect/
│       ├── SKILL.md
│       └── references/...
├── test/
│   ├── evals.json
│   ├── triggers.json
│   └── README.md
└── evals-workspace/                  # gitignored
    └── iteration-<N>/
        ├── <eval-id>/
        │   ├── with_skill/
        │   │   ├── outputs/          # the generated system prompt + any extra response text
        │   │   ├── timing.json       # { "total_tokens": ..., "duration_ms": ... }
        │   │   └── grading.json      # { "assertion_results": [...], "summary": {...} }
        │   └── without_skill/
        │       ├── outputs/
        │       ├── timing.json
        │       └── grading.json
        └── benchmark.json            # aggregated stats across all evals in this iteration
```

`with_skill` runs load `SKILL.md` and the references the skill chooses to read. `without_skill` runs use the same model and the same prompt without the skill loaded; this is the baseline that tells you whether the skill is actually adding value.

## Running an output-quality eval

For each `eval` in `evals.json`:

1. **Spawn the run.** Send a fresh agent (Claude or whatever harness you use) the request below. Save its full final response to `outputs/system_prompt.md`.

   ```
   You are about to act on a real user request. Use the skill at <SKILL_PATH> if applicable.

   User request:
   <eval.prompt>

   Save the final deliverable system prompt to <outputs_dir>/system_prompt.md.
   ```

   Also run the same `<eval.prompt>` with no skill loaded into `without_skill/outputs/system_prompt.md`.

2. **Capture timing.** Write tokens used and wall-clock duration to `timing.json`:
   ```json
   { "total_tokens": 0, "duration_ms": 0 }
   ```

3. **Grade.** For each assertion in the eval, write a result to `grading.json`. Require concrete evidence for `passed: true`. Conditional assertions that do not apply to this output are recorded with `applicable: false` and excluded from `total` / `pass_rate`:
   ```json
   {
     "assertion_results": [
       { "text": "<assertion>", "applies_when": null, "applicable": true, "passed": true, "evidence": "Verbatim quote or substring location from outputs/system_prompt.md" },
       { "text": "<assertion>", "applies_when": "the response drafts a prompt", "applicable": false, "passed": null, "evidence": "skipped: response is clarification-only" }
     ],
     "summary": { "passed": 0, "failed": 0, "skipped": 0, "total": 0, "pass_rate": 0.0 }
   }
   ```

4. **Aggregate.** Roll the per-eval grading into `benchmark.json`:
   ```json
   {
     "run_summary": {
       "with_skill":    { "pass_rate": { "mean": 0.0, "stddev": 0.0 }, "tokens": { "mean": 0, "stddev": 0 } },
       "without_skill": { "pass_rate": { "mean": 0.0, "stddev": 0.0 }, "tokens": { "mean": 0, "stddev": 0 } },
       "delta": { "pass_rate": 0.0, "tokens": 0 }
     }
   }
   ```

Most assertions in `evals.json` are written so they can be checked by simple substring or regex first, then by an LLM judge if a substring check is not enough. Examples:

- `does not contain the substring 'PushMessageDraft'` — string check.
- `the role line contains at least one profession-style noun from the set {...}` — string-set check on the line that introduces the role.
- `the missing-input rule asks the agent to say what is missing and skip generation` — LLM judge with the cited section as evidence.

### Conditional assertions

When an assertion only applies to one of several valid response shapes (e.g., "the role names a profession" only makes sense if the response contains a drafted prompt, not if it only asks clarifying questions), wrap it as an object instead of a string:

```json
{
  "text": "The drafted prompt names a real professional role and a specific domain",
  "applies_when": "the response contains a drafted system prompt for the target agent (not just clarification questions)"
}
```

The LLM grader first decides whether `applies_when` holds against the output. If it does not, the assertion is marked `applicable: false` and excluded from the case's `total` and `pass_rate` (the case is scored as `passed / applicable_count`). This prevents outputs that take a different but still-valid path from being penalized for assertions that target another path.

Plain-string assertions remain supported and are treated as always-applicable. Use conditional form only when the assertion text would otherwise need an `If ...` prefix or would be meaningless against a valid alternative output shape.

## Running a triggering eval

`triggers.json` is for tuning the skill's description, not its body. For each query:

1. Present a fresh agent with all available skill metadata (name + description), no SKILL.md content loaded.
2. Ask the agent to decide which skill, if any, to use for the query. Record `selected: true|false` for this skill.
3. Compare against `should_trigger`. Compute pass rate on `train` and `validation` separately.
4. If iterating on the description:
   - Use only `train` failures to drive description edits.
   - Use `validation` only to verify the final description generalizes.
   - Keep the description under 1024 characters.
   - Do not add specific keywords from failed queries; abstract the underlying concept instead.

## Grading principles

These mirror agentskills.io grading guidance and apply to both files:

- **Require concrete evidence for a PASS.** A section labeled "Output contract" with one vague sentence does not satisfy "describes the output format with section labels and a completion criterion". Cite the exact lines as evidence.
- **Review the assertions, not just the results.** While grading, flag assertions that always pass in both `with_skill` and `without_skill` (they aren't measuring skill value), assertions that always fail in both (probably broken or too strict), and assertions that aren't verifiable from the saved output alone.
- **Generalize from failures.** If the same kind of failure shows up across multiple evals (e.g., schema names leaking, role being a verb-plus-代理), fix the underlying SKILL.md rule rather than adding a narrow patch.

## Iteration loop

1. Run all `evals.json` cases at iteration `N` in both `with_skill/` and `without_skill/`. Compute `benchmark.json`.
2. Inspect failures. Look at whether the skill provided value over the baseline (delta in pass rate).
3. Decide one of:
   - Edit `SKILL.md` or a reference file to address the failure pattern.
   - Loosen or rewrite an assertion that turned out to be unverifiable or too brittle.
   - Add a missing test case if a real failure mode is uncovered that no eval catches.
4. Bump to iteration `N+1` and re-run.
5. Stop when pass rate plateaus or critical failure modes (runtime leakage, brand-name role) are at zero across the validation set.

## When to add or change a test case

Add a case when:
- A new failure mode shows up in real usage that no current case would catch.
- A reference file gains a rule that needs an empirical signal to confirm it changes behavior.

Rewrite an assertion when:
- It always passes regardless of skill quality (replace with one that distinguishes good from bad).
- It is too brittle (e.g., requires an exact phrase) and fails on equally-correct outputs.
- It cannot be verified from the saved output alone.

Do not add a case just because it would be nice to have — every case has a per-iteration cost in tokens and grading time.
