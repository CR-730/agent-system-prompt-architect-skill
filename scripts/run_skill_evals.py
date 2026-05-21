from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-system-prompt-architect"
EVALS_DIR = ROOT / "test"
WORKSPACE_DIR = ROOT / "evals-workspace"


@dataclass
class CallResult:
    content: str
    duration_ms: int
    total_tokens: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_client() -> OpenAI:
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("MIMO_API_KEY")
    base_url = os.getenv("MIMO_BASE_URL")
    if not api_key or not base_url:
        raise SystemExit("Set MIMO_API_KEY and MIMO_BASE_URL in the environment or .env before running.")
    return OpenAI(api_key=api_key, base_url=base_url, timeout=90, max_retries=1)


def chat(client: OpenAI, messages: list[dict[str, str]], temperature: float = 0.2) -> CallResult:
    model = os.getenv("MIMO_MODEL", "mimo-v2.5-pro")
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    duration_ms = int((time.perf_counter() - started) * 1000)
    content = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0)
    return CallResult(content=content.strip(), duration_ms=duration_ms, total_tokens=total_tokens)


def json_from_model(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"(\{.*\}|\[.*\])", cleaned, flags=re.S)
    if not match:
        raise ValueError(f"Model did not return JSON: {text[:500]}")
    return json.loads(match.group(1))


def skill_package() -> str:
    parts = [("# SKILL.md", read_text(SKILL_DIR / "SKILL.md"))]
    for path in sorted((SKILL_DIR / "references").glob("*.md")):
        parts.append((f"# references/{path.name}", read_text(path)))
    return "\n\n".join(f"{title}\n\n{body}" for title, body in parts)


def generation_messages(prompt: str, with_skill: bool) -> list[dict[str, str]]:
    if with_skill:
        system = (
            "You are evaluating a Codex skill. Use the provided skill package exactly as operational guidance. "
            "Return only the final answer that the skill would deliver to the user.\n\n"
            f"<skill_package>\n{skill_package()}\n</skill_package>"
        )
    else:
        system = (
            "You help users write system prompts for agents. Return the best answer you can. "
            "Do not mention that no skill is loaded."
        )
    user = (
        "User request:\n"
        f"{prompt}\n\n"
        "Produce the final response. If a deployable system prompt is possible, output the deployable prompt text. "
        "If the request is too underspecified, ask the minimal necessary clarifying questions."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def deterministic_assertion(assertion: str, output: str) -> dict[str, Any] | None:
    lowered = assertion.lower()
    quoted = re.findall(r"'([^']+)'|`([^`]+)`", assertion)
    terms = [a or b for a, b in quoted]

    if "does not contain" in lowered and terms:
        offenders = [term for term in terms if term in output]
        return {
            "text": assertion,
            "passed": not offenders,
            "evidence": "No forbidden substrings found." if not offenders else f"Found forbidden substrings: {offenders}",
            "grader": "rule",
        }

    if "contains at least one profession-style noun" in lowered:
        match = re.search(r"\{([^}]+)\}", assertion)
        if match:
            nouns = [item.strip() for item in match.group(1).split(",")]
            found = [noun for noun in nouns if noun and noun in output]
            return {
                "text": assertion,
                "passed": bool(found),
                "evidence": f"Found profession-style nouns: {found}" if found else "No listed profession-style noun found.",
                "grader": "rule",
            }

    if "does not end with" in lowered and terms:
        lines = role_like_lines(output)
        bad = [line for line in lines if any(line.strip().endswith(term) for term in terms)]
        return {
            "text": assertion,
            "passed": not bad,
            "evidence": "No role-like line ends with forbidden suffix." if not bad else f"Forbidden role lines: {bad[:3]}",
            "grader": "rule",
        }

    return None


def role_like_lines(output: str) -> list[str]:
    candidates = []
    for line in output.splitlines():
        stripped = line.strip(" #*-")
        if not stripped:
            continue
        if any(token in stripped for token in ["You are", "你是", "Role", "角色"]):
            candidates.append(stripped)
    return candidates[:8]


def normalize_assertion(item: Any) -> dict[str, Any]:
    if isinstance(item, str):
        return {"text": item, "applies_when": None}
    if isinstance(item, dict) and "text" in item:
        return {"text": str(item["text"]), "applies_when": item.get("applies_when")}
    raise ValueError(f"Unsupported assertion shape: {item!r}")


def llm_grade(client: OpenAI, output: str, assertions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not assertions:
        return []
    items = [
        {"index": idx, "text": a["text"], "applies_when": a["applies_when"]}
        for idx, a in enumerate(assertions)
    ]
    prompt = {
        "output": output,
        "assertions": items,
        "instructions": (
            "For each assertion, perform two steps in order. "
            "Step 1 \u2014 Applicability check: if 'applies_when' is non-null, decide whether that condition is true based on the output; "
            "if it is NOT true, return {\"applicable\": false, \"passed\": null, \"evidence\": \"skipped: <one-line reason>\"}. "
            "If 'applies_when' is null, treat the assertion as always applicable. "
            "Step 2 \u2014 Grading (only when applicable): decide whether the assertion holds based on concrete evidence from the output; "
            "return {\"applicable\": true, \"passed\": true|false, \"evidence\": \"<quote or concise reason>\"}. "
            "A pass requires concrete evidence; if uncertain, mark passed=false. "
            "Return JSON only: {\"results\":[{\"index\": int, \"applicable\": bool, \"passed\": bool|null, \"evidence\": str}]}. "
            "Include one result per input assertion, preserving 'index'."
        ),
    }
    result = chat(
        client,
        [
            {"role": "system", "content": "You are a strict evaluator for agent system-prompt quality."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        temperature=0,
    )
    data = json_from_model(result.content)
    by_index = {int(item.get("index", -1)): item for item in data.get("results", [])}
    out: list[dict[str, Any]] = []
    for idx, assertion in enumerate(assertions):
        item = by_index.get(idx, {})
        applicable = bool(item.get("applicable", True))
        passed_raw = item.get("passed")
        passed = bool(passed_raw) if applicable and passed_raw is not None else None
        out.append(
            {
                "text": assertion["text"],
                "applies_when": assertion["applies_when"],
                "applicable": applicable,
                "passed": passed,
                "evidence": item.get("evidence", ""),
                "grader": "llm" if applicable else "skipped",
            }
        )
    return out


def grade_output(client: OpenAI, output: str, assertions: list[Any]) -> dict[str, Any]:
    normalized = [normalize_assertion(a) for a in assertions]
    results: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for assertion in normalized:
        if assertion["applies_when"] is not None:
            unresolved.append(assertion)
            continue
        rule_result = deterministic_assertion(assertion["text"], output)
        if rule_result is None:
            unresolved.append(assertion)
        else:
            rule_result["applies_when"] = None
            rule_result["applicable"] = True
            results.append(rule_result)
    results.extend(llm_grade(client, output, unresolved))

    applicable = [r for r in results if r.get("applicable", True)]
    passed = sum(1 for r in applicable if r.get("passed"))
    total = len(applicable)
    skipped = len(results) - total
    return {
        "assertion_results": results,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "skipped": skipped,
            "total": total,
            "pass_rate": passed / total if total else 0.0,
        },
    }


def run_quality(client: OpenAI, iteration_dir: Path, with_baseline: bool, limit: int | None, case_filter: list[str] | None) -> dict[str, Any]:
    evals = json.loads(read_text(EVALS_DIR / "evals.json"))["evals"]
    if case_filter:
        wanted = set(case_filter)
        evals = [c for c in evals if c["id"] in wanted]
        missing = wanted - {c["id"] for c in evals}
        if missing:
            raise SystemExit(f"Unknown case ids in --case filter: {sorted(missing)}")
    if limit is not None:
        evals = evals[:limit]

    modes = ["with_skill", "without_skill"] if with_baseline else ["with_skill"]
    summaries: dict[str, list[dict[str, Any]]] = {mode: [] for mode in modes}

    for case in evals:
        for mode in modes:
            run_dir = iteration_dir / case["id"] / mode
            generated = chat(client, generation_messages(case["prompt"], with_skill=(mode == "with_skill")))
            write_text(run_dir / "outputs" / "system_prompt.md", generated.content + "\n")
            write_json(run_dir / "timing.json", {"total_tokens": generated.total_tokens, "duration_ms": generated.duration_ms})
            grading = grade_output(client, generated.content, case["assertions"])
            write_json(run_dir / "grading.json", grading)
            summaries[mode].append({"id": case["id"], "tokens": generated.total_tokens, **grading["summary"]})

    return {"quality": aggregate_quality(summaries)}


def mean(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def stdev(values: list[float]) -> float:
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def aggregate_quality(summaries: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for mode, rows in summaries.items():
        rates = [float(row["pass_rate"]) for row in rows]
        tokens = [float(row["tokens"]) for row in rows]
        out[mode] = {
            "cases": rows,
            "pass_rate": {"mean": mean(rates), "stddev": stdev(rates)},
            "tokens": {"mean": mean(tokens), "stddev": stdev(tokens)},
        }
    if "with_skill" in out and "without_skill" in out:
        out["delta"] = {
            "pass_rate": out["with_skill"]["pass_rate"]["mean"] - out["without_skill"]["pass_rate"]["mean"],
            "tokens": out["with_skill"]["tokens"]["mean"] - out["without_skill"]["tokens"]["mean"],
        }
    return out


def skill_description() -> str:
    text = read_text(SKILL_DIR / "SKILL.md")
    match = re.search(r"^description:\s*(.+)$", text, flags=re.M)
    if not match:
        raise RuntimeError("SKILL.md has no description field.")
    return match.group(1).strip().strip('"')


def run_triggers(client: OpenAI, iteration_dir: Path) -> dict[str, Any]:
    queries = json.loads(read_text(EVALS_DIR / "triggers.json"))["queries"]
    payload = {
        "skill": {"name": "agent-system-prompt-architect", "description": skill_description()},
        "queries": [{"index": idx, "query": item["query"]} for idx, item in enumerate(queries)],
        "instructions": (
            "For each query, decide whether this skill should be selected. Return JSON only: "
            "{\"decisions\":[{\"index\":0,\"selected\":true|false,\"reason\":\"...\"}]}"
        ),
    }
    result = chat(
        client,
        [
            {"role": "system", "content": "You evaluate skill-trigger metadata. Use only the name and description, not SKILL.md contents."},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        temperature=0,
    )
    data = json_from_model(result.content)
    by_index = {int(item["index"]): item for item in data.get("decisions", [])}
    rows = []
    for idx, query in enumerate(queries):
        decision = by_index.get(idx, {})
        selected = bool(decision.get("selected", False))
        rows.append(
            {
                "index": idx,
                "set": query["set"],
                "query": query["query"],
                "should_trigger": bool(query["should_trigger"]),
                "selected": selected,
                "passed": selected == bool(query["should_trigger"]),
                "reason": decision.get("reason", ""),
            }
        )
    summary = aggregate_triggers(rows)
    write_json(iteration_dir / "trigger_eval.json", {"rows": rows, "summary": summary, "timing": {"total_tokens": result.total_tokens, "duration_ms": result.duration_ms}})
    return {"triggers": summary}


def aggregate_triggers(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for split in ["train", "validation", "all"]:
        subset = rows if split == "all" else [row for row in rows if row["set"] == split]
        total = len(subset)
        passed = sum(1 for row in subset if row["passed"])
        summary[split] = {"passed": passed, "failed": total - passed, "total": total, "pass_rate": passed / total if total else 0.0}
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run evals for agent-system-prompt-architect.")
    parser.add_argument("--quality", action="store_true", help="Run output-quality evals.")
    parser.add_argument("--triggers", action="store_true", help="Run trigger evals.")
    parser.add_argument("--with-baseline", action="store_true", help="Run without-skill baseline for quality evals.")
    parser.add_argument("--limit", type=int, default=None, help="Limit quality evals to the first N cases.")
    parser.add_argument("--case", action="append", default=None, help="Run only the named case id(s); repeatable.")
    parser.add_argument("--iteration", default=None, help="Override iteration directory name.")
    args = parser.parse_args()

    if not args.quality and not args.triggers:
        args.quality = True
        args.triggers = True

    client = load_client()
    iteration_name = args.iteration or f"iteration-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    iteration_dir = WORKSPACE_DIR / iteration_name
    iteration_dir.mkdir(parents=True, exist_ok=True)

    benchmark: dict[str, Any] = {"iteration": iteration_name, "model": os.getenv("MIMO_MODEL", "mimo-v2.5-pro")}
    if args.quality:
        benchmark.update(run_quality(client, iteration_dir, with_baseline=args.with_baseline, limit=args.limit, case_filter=args.case))
    if args.triggers:
        benchmark.update(run_triggers(client, iteration_dir))

    write_json(iteration_dir / "benchmark.json", benchmark)
    print(json.dumps({"iteration_dir": str(iteration_dir), **benchmark}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
