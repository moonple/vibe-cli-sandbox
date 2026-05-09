# vibe-cli-sandbox

用于 AI coding agent 评测/演示（Python, CLI）。

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Demo (Generate)

Run a demo task and write structured output to JSON:

```bash
vibe run --repo . --task "timing smoke test" --out out.md --json-out out.json
```

Check the observability fields (request_id / timings / error) in JSON:

```bash
python - <<'PY'
import json
d=json.load(open("out.json","r",encoding="utf-8"))
print("request_id:", d.get("request_id"))
print("timings_ms:", d.get("timings_ms"))
print("error:", d.get("error"))
PY
```

Notes:
- `out.md` / `out.json` are generated outputs (gitignored by default).

## Eval

Run the evaluation suite:

```bash
python eval/run_cases.py
```

- Cases: `eval/cases_v0.json`
- Runner: `eval/run_cases.py`
- Output: `eval/report.json` (gitignored)
