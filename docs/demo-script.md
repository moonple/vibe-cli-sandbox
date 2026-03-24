# Demo Script (3 minutes)

目标：演示 vibe-cli-sandbox 作为 AI coding agent 的评测/演示最小闭环：生成输出 -> 结构化可观测 -> 可评测回归。

## 0. 准备（30s）

在仓库根目录：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

说明：
- `vibe` 是通过 editable install 安装的 CLI entrypoint。
- 输出文件 `out.md/out.json` 默认是生成物（已在 `.gitignore` 中忽略）。

## 1. Demo：生成一次任务输出（60s）

运行 demo（生成 Markdown + JSON）：

```bash
vibe run --repo . --task "timing smoke test" --out out.md --json-out out.json
```

打开并解释 `out.json` 中关键字段（结构化、可被平台采集/聚合）：

- `request_id`：本次运行唯一标识，可用于串联日志/评测/回放
- `timings_ms.total_ms`：端到端耗时（以及分阶段耗时，如 `validate_repo_ms` 等）
- `error`：失败时的结构化错误（type/message/details）
- `plan`：生成的执行计划（用于质量门槛/回归）
- `changes`：变更摘要/patch（当前为 mock，但结构已固定）

快速查看字段（可选）：

```bash
python - <<'PY'
import json
d=json.load(open("out.json","r",encoding="utf-8"))
print("request_id:", d.get("request_id"))
print("timings_ms:", d.get("timings_ms"))
print("error:", d.get("error"))
print("plan_len:", len(d.get("plan") or []))
print("changes:", len(d.get("changes") or []))
PY
```

## 2. Eval：跑用例集与质量门槛（60s）

运行 eval：

```bash
python eval/run_cases.py
```

产物：
- `eval/report.json`：机器可读结果（gitignored）
- `eval/report.md`：人类可读报告（gitignored）

展示 `eval/report.md` 的关键信息：
- `pass_rate`
- `fail_types`（失败类型分布）
- `timing_total_ms`（性能统计）
- case 级别的 `plan_len`（用于“质量门槛”，证明评测可以卡住不合格输出）

说明：
- 当前用例集中包含一个“故意卡门槛”的 case，用于证明 eval 能区分质量好坏（不会永远 100%）。

## 3. 收尾（30s）

结论：
- 已跑通从 “生成输出” 到 “可观测字段” 到 “评测回归报告” 的最小闭环。
- 后续可以把 mock runner 替换为真实 LLM/agent 实现，而 eval/报告体系保持不变。
