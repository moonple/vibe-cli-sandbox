# Demo Script (3 minutes)

目标：演示 vibe-cli-sandbox 作为 AI coding agent 评测/演示的最小闭环：生成输出 -> 结构化可观测 -> 可评测回归。

## 0. 准备（30s）

先 cd 到仓库根目录cd ~/projects/vibe-cli-sandbox
在仓库根目录：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

说明：
- `vibe` 是通过 editable install 安装的 CLI entrypoint。
- 输出文件默认是生成物（已在 `.gitignore` 中忽略）。

## 1. Demo：成功任务输出（45s）

运行 demo（生成 Markdown + JSON）：

```bash
vibe run --repo . --task "timing smoke test" --out out.success.md --json-out out.success.json
```

打开并解释 `out.success.json` 中关键字段（结构化、可被平台采集/聚合）：

- `request_id`：本次运行唯一标识，可用于串联日志/评测/回放
- `timings_ms.total_ms`：端到端耗时（以及分阶段耗时，如 `validate_repo_ms` 等）
- `plan`：生成的执行计划（用于质量门槛/回归）
- `changes`：变更摘要/patch（当前为 mock，但结构已固定）
- `error`：成功时为 `null`

快速查看字段（可选）：

```bash
python - <<'PY2'
import json
d=json.load(open("out.success.json","r",encoding="utf-8"))
print("request_id:", d.get("request_id"))
print("timings_ms:", d.get("timings_ms"))
print("plan_len:", len(d.get("plan") or []))
print("changes:", len(d.get("changes") or []))
print("error:", d.get("error"))
PY2
```

## 2. Demo：失败场景（30s）

展示失败时的结构化输出：

```bash
vibe run --repo ./__repo_does_not_exist__ --task "test" --json-out out.fail.json
cat out.fail.json | python -m json.tool
```

关键观察：
- `success: false` - 任务失败
- `error.type: repo_not_found` - 结构化错误类型
- `plan: []` - 失败时计划为空（字段仍然存在）
- `timings_ms` - 仍然记录耗时（用于监控）

结论：**失败也可观测、可评测**。

## 3. Eval：跑用例集与质量门槛（60s）

运行 eval：

```bash
python eval/run_cases.py
```

产物：
- `eval/report.json`：机器可读结果（gitignored）
- `eval/report.md`：人类可读报告（gitignored）

展示 `eval/report.md` 的关键信息：
- `pass_rate`：不是 100%（证明评测能发现问题）
- `fail_types`：失败类型分布（例如 `repo_not_found` / `fail_plan_too_short`）
- `timing_total_ms`：性能统计（mean/p50/p95）
- case 级别的 `plan_len`：展示质量门槛（plan 长度不足会失败）

## 4. 收尾（15s）

结论：
- ✅ 结构化输出（JSON）：request_id / timings_ms / plan / changes / error
- ✅ 可观测性：成功/失败都可追踪、可分析
- ✅ 评测驱动：自动化测试 + 质量门槛（不再是永远 100%）
- ✅ 可扩展：后续可替换为真实 LLM/agent，而 eval/报告体系保持不变
