# Eval Cases v0 (Week4)

> Goal: establish a repeatable evaluation set (cases) for coding-agent performance.
>
> Repo under test: `moonple/vibe-cli-sandbox`
> Date: 2026-05-09
>
> Scoring: each case suggests an **auto** (rule-based) and **manual** (human) score split. You can keep the rubric in `eval/report_v0.md`.

## Case format
Each case includes:
- **type**: bugfix / function / test / refactor
- **setup**: commands to prepare environment
- **task**: the prompt you give to the agent
- **verification**: how to verify (commands)
- **expected**: objective pass/fail criteria
- **scoring**: suggested score split

---

## case_001 (bugfix) — json_out permission fallback
- type: bugfix
- setup:
  - `python -m pip install -e .`
- task:
  - When `--json-out` points to a non-writable path (e.g. under `/root/`), the CLI should:
    1) mark the run as end-to-end failure (`success=false`)
    2) write an error JSON to a fallback path `./out.error.json`
    3) exit with code 1
- verification:
  - `rm -f out.error.json`
  - `vibe run --repo . --task "timing smoke test" --json-out /root/out.runtime.json; echo $?`
  - `test -f out.error.json`
  - `python -c "import json; d=json.load(open('out.error.json')); print(d['success'], (d.get('error') or {}).get('type'))"`
- expected:
  - exit code = 1
  - `out.error.json` exists
  - JSON contains: `success=false`, `error.type=runtime_error`, and non-empty `request_id`
- scoring:
  - auto: 6
  - manual: 4
- notes:
  - This case is intentionally environment-dependent: `/root/` should be non-writable for a normal user.

## case_002 (bugfix) — invalid_input: empty task
- type: bugfix
- setup:
  - `python -m pip install -e .`
- task:
  - If `--task` is an empty string, the CLI must:
    1) exit with code 1
    2) write a JSON (if `--json-out` provided) with `error.type=invalid_input` and `timings_ms.total_ms=0.0`
    3) include a helpful `fallback` list
- verification:
  - `vibe run --repo . --task "" --json-out /tmp/out.invalid_empty.json; echo $?`
  - `python -c "import json; d=json.load(open('/tmp/out.invalid_empty.json')); print(d['success'], d['error']['type'], d['timings_ms'].get('total_ms'), len(d.get('fallback',[])))"`
- expected:
  - exit code = 1
  - JSON: `success=false`, `error.type=invalid_input`, `total_ms=0.0`, `fallback` length > 0
- scoring:
  - auto: 7
  - manual: 3

## case_003 (bugfix) — invalid_input: whitespace-only task
- type: bugfix
- setup:
  - `python -m pip install -e .`
- task:
  - If `--task` is whitespace-only (e.g. `"   "`), treat it as empty input and behave like case_002.
- verification:
  - `vibe run --repo . --task "   " --json-out /tmp/out.invalid_spaces.json; echo $?`
  - `python -c "import json; d=json.load(open('/tmp/out.invalid_spaces.json')); print(d['error']['type'], d['message'])"`
- expected:
  - exit code = 1
  - JSON: `error.type=invalid_input`
- scoring:
  - auto: 7
  - manual: 3

## case_004 (bugfix) — repo_not_found classification
- type: bugfix
- setup:
  - `python -m pip install -e .`
- task:
  - If `--repo` points to a non-existing path, the runner/CLI must fail with:
    - `success=false`
    - `error.type=repo_not_found`
    - non-empty `fallback`
    - exit code 1
- verification:
  - `vibe run --repo /path/does/not/exist --task test --json-out /tmp/out.repo_missing.json; echo $?`
  - `python -c "import json; d=json.load(open('/tmp/out.repo_missing.json')); print(d['error']['type'], len(d.get('fallback',[])))"`
- expected:
  - exit code = 1
  - JSON: `error.type=repo_not_found`
  - `fallback` length > 0
- scoring:
  - auto: 7
  - manual: 3

## case_005 (test) — add tests for invalid_input and repo_not_found
- type: test
- setup:
  - `python -m pip install -e .`
  - `python -m pip install pytest`
- task:
  - Add pytest coverage for:
    1) `--task ""` produces `invalid_input` JSON and exits 1
    2) missing repo path produces `repo_not_found` JSON and exits 1
  - Tests should avoid writing to `/root/`.
- verification:
  - `pytest -q; echo $?`
- expected:
  - exit code = 0
  - at least 2 tests added; assertions check `error.type` and exit codes
- scoring:
  - auto: 5
  - manual: 5
- notes:
  - Preferred: invoke the CLI entrypoint as a function (if exposed) or call the module with `python -m` in subprocess.

## case_006 (refactor) — remove duplicated imports and dead code in cli.py
- type: refactor
- setup:
  - `python -m pip install -e .`
- task:
  - In `src/vibe_cli_sandbox/cli.py`, remove duplicated imports and unused helpers/variables (e.g. repeated `Path` import, unused `_write_text_safely`, unused flags) without changing behavior.
- verification:
  - `python -m py_compile src/vibe_cli_sandbox/cli.py; echo $?`
  - `vibe run --repo . --task "timing smoke test" --json-out /tmp/out.refactor_smoke.json; echo $?`
- expected:
  - compile OK
  - smoke run exit code = 0
- scoring:
  - auto: 4
  - manual: 6

## case_007 (function) — CLI option: --trace-dir to archive JSON outputs
- type: function
- setup:
  - `python -m pip install -e .`
- task:
  - Add a new optional CLI option `--trace-dir`.
  - If provided, after each run (success or failure), write/copy the final JSON output into `trace_dir/<request_id>.json`.
  - If JSON output path is unwritable, the archived copy should use the fallback JSON that was actually written.
- verification:
  - `rm -rf /tmp/vibe_traces && mkdir -p /tmp/vibe_traces`
  - `vibe run --repo . --task "timing smoke test" --json-out /tmp/out.ok.json --trace-dir /tmp/vibe_traces; echo $?`
  - `ls -1 /tmp/vibe_traces | head`
- expected:
  - exit code = 0
  - `/tmp/vibe_traces/` contains exactly one new `*.json` file
  - archived JSON has same `request_id` as printed in Run Summary
- scoring:
  - auto: 6
  - manual: 4
- notes:
  - This case is a small feature that improves repeatability for Week4+.

## case_008 (test) — test --trace-dir behavior
- type: test
- setup:
  - `python -m pip install -e .`
  - `python -m pip install pytest`
- task:
  - Add pytest coverage for the `--trace-dir` option (case_007):
    - it creates `<request_id>.json`
    - contents are valid JSON and include matching request_id
- verification:
  - `pytest -q; echo $?`
- expected:
  - exit code = 0
- scoring:
  - auto: 5
  - manual: 5

## case_009 (bugfix) — ensure typer.Exit(1) is not double-handled
- type: bugfix
- setup:
  - `python -m pip install -e .`
- task:
  - Ensure that when the CLI intentionally exits via `typer.Exit(1)` (e.g. after a known failure), it is not caught by the generic exception handler and re-logged as `❌ Error: 1`.
  - Add or keep a dedicated `except typer.Exit: raise` to avoid double-reporting.
- verification:
  - Run a known failure case and confirm output does NOT include the substring `"❌ Error: 1"`.
  - Example: `vibe run --repo /path/does/not/exist --task test --json-out /tmp/out.repo_missing.json`
- expected:
  - output does not include `❌ Error: 1`
- scoring:
  - auto: 3
  - manual: 7
- notes:
  - This is mostly a regression guard.

## case_010 (refactor) — unify ErrorInfo usage and types
- type: refactor
- setup:
  - `python -m pip install -e .`
- task:
  - Make sure all code paths construct `TaskResult.error` consistently as `ErrorInfo` (not a raw dict), and `ErrorInfo.details` respects the declared type.
  - Keep output JSON schema stable.
- verification:
  - Run case_001 and case_004; then validate JSON contains `error.details` as string or null.
  - `python -c "import json; d=json.load(open('out.error.json')); print(type(d['error'].get('details')).__name__)"`
- expected:
  - `error.details` is either `None` or `str` (never dict)
- scoring:
  - auto: 4
  - manual: 6

---

## Next
Add cases 011-030 (tests, refactors, and feature tasks) to reach Week4's required 30 cases.
