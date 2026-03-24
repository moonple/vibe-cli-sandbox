from __future__ import annotations

import json
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CaseResult:
    id: str
    ok: bool
    expect_success: bool
    actual_success: bool
    error_type: str | None
    error_message: str | None
    request_id: str | None
    timings_ms: dict[str, float]
    duration_ms: float
    plan: list[str]
    reason: str | None


def _pctl(values: list[float], p: float) -> float:
    """Nearest-rank percentile (good enough for small N)."""
    if not values:
        return 0.0
    values_sorted = sorted(values)
    k = int(round((p / 100.0) * (len(values_sorted) - 1)))
    k = max(0, min(k, len(values_sorted) - 1))
    return float(values_sorted[k])


def render_markdown_report(report: dict) -> str:
    """Generate human-readable markdown report from eval results."""
    meta = report["meta"]
    fail_types = report.get("fail_types", {})
    timing = report.get("timing_total_ms", {})
    cases = report.get("cases", [])

    lines = []
    lines.append("# Eval Report\n\n")
    lines.append(f"- Total cases: {meta['total_cases']}\n")
    lines.append(f"- Passed cases: {meta['passed_cases']}\n")
    lines.append(f"- Pass rate: {meta['pass_rate']:.2%}\n\n")

    lines.append("## Failure types\n\n")
    if not fail_types:
        lines.append("- None\n")
    else:
        for k, v in fail_types.items():
            lines.append(f"- {k}: {v}\n")
    lines.append("\n")

    quality_fail_types = report.get("quality_fail_types", {})
    lines.append("## Quality gate failures (ok=false but actual_success=true)\n\n")
    if not quality_fail_types:
        lines.append("- None\n")
    else:
        for k, v in quality_fail_types.items():
            lines.append(f"- {k}: {v}\n")
    lines.append("\n")

    lines.append("## Timing stats (timings_ms.total_ms)\n\n")
    if timing:
        for k in ["count", "mean_ms", "p50_ms", "p95_ms", "min_ms", "max_ms"]:
            if k in timing:
                val = timing[k]
                if isinstance(val, (int, float)):
                    lines.append(f"- {k}: {val:.3f}ms\n")
                else:
                    lines.append(f"- {k}: {val}\n")
    else:
        lines.append("- No timing data\n")
    lines.append("\n")

    lines.append("## Case details\n\n")
    lines.append("| id | ok | actual_success | error_type | reason | total_ms | plan_len |\n")
    lines.append("|---|---:|---:|---:|---|---:|---:|\n")
    for c in cases:
        total_ms = (c.get("timings_ms") or {}).get("total_ms", 0.0)
        plan_len = len(c.get("plan", [])) if c.get("plan") else 0
        reason = c.get("reason") or ""
        lines.append(
            f"| {c['id']} | {'✅' if c['ok'] else '❌'} | "
            f"{'✅' if c['actual_success'] else '❌'} | "
            f"{c.get('error_type') or ''} | {reason} | {float(total_ms):.3f} | {plan_len} |\n"
        )

    return "".join(lines)


def run_case(case: dict[str, Any]) -> CaseResult:
    from vibe_cli_sandbox.models import TaskConfig
    from vibe_cli_sandbox.runner import run_task

    t0 = time.perf_counter()
    cfg = TaskConfig(repo_path=case["repo"], task_description=case["task"])
    res = run_task(cfg)
    dur_ms = (time.perf_counter() - t0) * 1000.0

    err_type = (res.error.type if res.error else None)
    err_msg = (res.error.message if res.error else None)

    ok = True
    if bool(res.success) != bool(case.get("expect_success", True)):
        ok = False

    if "expect_error_type" in case:
        if err_type != case["expect_error_type"]:
            ok = False

    # Basic schema checks (platform-ish)
    if not res.request_id:
        ok = False
    if not isinstance(res.timings_ms, dict) or "total_ms" not in res.timings_ms:
        ok = False
    
    # Plan quality check
    reason: str | None = None
    if "expect_min_plan_len" in case:
        min_len = case["expect_min_plan_len"]
        if not getattr(res, "plan", None) or len(res.plan) < min_len:
            ok = False
            reason = "plan_too_short"
            
    # If the run succeeded but the case failed, this is a quality-gate failure.
    # Ensure we always emit a stable reason key to avoid "unknown" in aggregation.
    if res.success and (not ok) and (reason is None):
        reason = "quality_gate_failed"
        
    return CaseResult(
        id=case["id"],
        ok=ok,
        expect_success=bool(case.get("expect_success", True)),
        actual_success=bool(res.success),
        error_type=err_type,
        error_message=err_msg,
        request_id=res.request_id,
        timings_ms=dict(res.timings_ms),
        duration_ms=dur_ms,
        plan=list(res.plan or []),
        reason=reason,
    )


def main() -> int:
    cases_path = Path(__file__).parent / "cases_v0.json"
    report_path = Path(__file__).parent / "report.json"

    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    results: list[CaseResult] = []
    for case in cases:
        results.append(run_case(case))

    total = len(results)
    passed = sum(1 for r in results if r.ok)
    success_rate = passed / total if total else 0.0

    # Failure type distribution (when actual_success is False)
    fail_types: dict[str, int] = {}
    for r in results:
        if not r.actual_success:
            key = r.error_type or "unknown"
            fail_types[key] = fail_types.get(key, 0) + 1
    # Quality gate failure distribution (when actual_success is True but ok is False)
    quality_fail_types: dict[str, int] = {}
    for r in results:
        if r.actual_success and (not r.ok):
            key = r.reason or "quality_gate_failed"
            quality_fail_types[key] = quality_fail_types.get(key, 0) + 1

    # Timing stats (take total_ms from timings_ms)
    total_ms_values = [
        float(r.timings_ms.get("total_ms", 0.0)) for r in results if r.timings_ms
    ]
    timing_stats = {}
    if total_ms_values:
        timing_stats = {
            "count": len(total_ms_values),
            "mean_ms": float(statistics.mean(total_ms_values)),
            "p50_ms": _pctl(total_ms_values, 50),
            "p95_ms": _pctl(total_ms_values, 95),
            "min_ms": float(min(total_ms_values)),
            "max_ms": float(max(total_ms_values)),
        }

    report = {
        "meta": {
            "cases_path": str(cases_path.relative_to(Path.cwd())),
            "total_cases": total,
            "passed_cases": passed,
            "pass_rate": success_rate,
        },
        "fail_types": fail_types,
        "quality_fail_types": quality_fail_types,
        "timing_total_ms": timing_stats,
        "cases": [
            {
                "id": r.id,
                "ok": r.ok,
                "expect_success": r.expect_success,
                "actual_success": r.actual_success,
                "error_type": r.error_type,
                "error_message": r.error_message,
                "request_id": r.request_id,
                "timings_ms": r.timings_ms,
                "duration_ms": r.duration_ms,
                "plan": r.plan,
                "reason": r.reason,
            }
            for r in results
        ],
    }

    # Write JSON report
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[eval] JSON report written to: {report_path}")

    # Write Markdown report
    report_md_path = Path(__file__).parent / "report.md"
    report_md_path.write_text(render_markdown_report(report), encoding="utf-8")
    print(f"[eval] Markdown report written to: {report_md_path}")

    # Print summary
    print(f"[eval] total={total} passed={passed} pass_rate={success_rate:.2%}")
    if fail_types:
        print(f"[eval] fail_types={fail_types}")
    if timing_stats:
        print(f"[eval] timing_total_ms={timing_stats}")

    # Exit non-zero if any case failed
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
