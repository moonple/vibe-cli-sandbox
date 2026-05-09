# Cross-Repo Sync Pack (2026-05-09)

目标：把 `moonple/vibe-cli-sandbox` 的可观测性与错误规范，同步到：

- `moonple/career-llm-plan`
- `moonple/llm-infer-deploy-lab`

---

## 1) 源仓库（vibe-cli-sandbox）当前基线总结

### 1.1 当前功能与任务运行流程

1. CLI 入口：`vibe run --repo <path> --task <text> [--out out.md] [--json-out out.json]`
2. 运行阶段：
   - 参数预检查（`task.strip()`）
   - `runner.run_task()`（校验 repo、生成结果）
   - 写 markdown/json 输出
3. 失败处理：
   - 输入非法：`invalid_input`
   - repo 路径不存在：`repo_not_found`
   - 运行期异常（含输出写文件失败）：`runtime_error`
4. 关键 fallback 约定：
   - 失败时 `fallback` 给出可执行下一步
   - `--json-out` 不可写时，降级写 `out.error.json`

### 1.2 输出可观测性约定（TaskResult）

- `request_id`：每次运行唯一 ID（trace/eval 串联主键）
- `success`：最终端到端是否成功
- `timings_ms.total_ms`：总耗时（失败也必须有）
- `error`：失败时结构化对象（`type/message/details`），成功时 `null`
- `commands/risks/fallback`：成功/失败都必须存在（可为空）

### 1.3 Week2 / Week3 规范要点

- Week2 输入与错误类型基线：
  - `invalid_input`
  - `repo_not_found`
  - `runtime_error`
  - `success baseline`（成功样本）
- Week3 trace 样本：
  - 在 `results/trace_samples.md` 记录 `request_id/success/total_ms/error.type/notes`
  - 推荐同时归档 `results/traces/*.json` 作为可复现证据

---

## 2) 目标仓库一：career-llm-plan 同步内容

仓库现状：以计划/提示词/周志为主，无独立 CLI 入口。建议同步“规范与模板”，并提供最小 JSON 产物生成方式。

### 2.1 README 新增段落（建议追加）

```markdown
## 任务执行与输出格式约定（Sync with vibe-cli-sandbox）

本仓库的计划任务记录采用统一 JSON 结构，字段与 vibe-cli-sandbox 对齐，便于后续汇总与评测：

- `request_id`: 本次任务唯一 ID
- `success`: 是否成功
- `timings_ms.total_ms`: 总耗时（毫秒）
- `error`: 失败时结构化错误（`type/message/details`）
- `fallback`: 失败时下一步建议（数组）

建议错误类型基线：
- `invalid_input`（输入为空/格式不合法）
- `repo_not_found`（引用路径不存在）
- `runtime_error`（其他运行时问题）
```

### 2.2 新增文件：`results/trace_samples.md`（模板）

````markdown
# Trace Samples

> 用于记录计划任务执行样本，保证 request_id / timings_ms / error.type 可追踪。

| # | date | request_id | task | success | total_ms | error.type | notes |
|---|---|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | <id> | weekly planning baseline | true | <ms> | - | success baseline |
| 2 | YYYY-MM-DD | <id> | empty objective | false | 0.0 | invalid_input | objective is empty |
| 3 | YYYY-MM-DD | <id> | missing context path | false | <ms> | repo_not_found | context file missing |
| 4 | YYYY-MM-DD | <id> | write artifact permission denied | false | 0.0 | runtime_error | fallback to local writable path |
```
````

### 2.3 新增文件：`prompts/task-result-template.md`

````markdown
# Task Result Prompt Template

请按以下 JSON 输出，不要省略字段：

```json
{
  "request_id": "<uuid>",
  "success": true,
  "message": "...",
  "commands": [],
  "risks": [],
  "fallback": [],
  "timings_ms": {"total_ms": 0.0},
  "error": null,
  "plan": [],
  "changes": []
}
```

失败时：
- `success=false`
- 填写 `error.type`（`invalid_input` / `repo_not_found` / `runtime_error`）
- 给出可执行 `fallback`
```
````

### 2.4 JSON 产物生成示例命令（与仓库结构匹配）

```bash
mkdir -p results/traces
python3 - <<'PY'
import json, time, uuid, pathlib
started = time.perf_counter()
out = {
  "request_id": uuid.uuid4().hex,
  "success": True,
  "message": "weekly planning baseline",
  "commands": ["update plans/weekly-log.md"],
  "risks": [],
  "fallback": [],
  "timings_ms": {"total_ms": round((time.perf_counter() - started) * 1000, 3)},
  "error": None,
  "plan": ["collect context", "update weekly log", "summarize next actions"],
  "changes": [{"file": "plans/weekly-log.md", "summary": "append week progress", "diff": None}]
}
path = pathlib.Path("results/traces/01_success_baseline.json")
path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(path)
PY
```

---

## 3) 目标仓库二：llm-infer-deploy-lab 同步内容

仓库现状：已有 `eval/run_cases.py`，可直接输出 `eval/report.json`；适合补齐“TaskResult 风格可观测约定 + trace 样本模板 + 失败 fallback 指引”。

### 3.1 README 新增段落（建议追加）

```markdown
## 任务执行与输出格式约定（Sync with vibe-cli-sandbox）

除 `eval/report.json` 外，建议统一记录以下可观测字段：

- `request_id`: 每次评测/调用唯一标识
- `success`: 本次运行是否成功（端到端）
- `timings_ms.total_ms`: 总耗时
- `error`: 结构化错误（`runtime_error` / `timeout_error` / `quality_error` / `config_error`）
- `fallback`: 失败后建议操作（例如切换 `--offline`、检查 server URL、缩短 case）

建议失败时总是保留 JSON 结果文件，便于 trace 回放。
```

### 3.2 新增文件：`results/trace_samples.md`（模板）

````markdown
# Trace Samples

| # | date | request_id | mode | case_id | success | total_ms | error.type | notes |
|---|---|---|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | <id> | offline | schema_check | true | <ms> | - | success baseline |
| 2 | YYYY-MM-DD | <id> | online | <case> | false | <ms> | runtime_error | server unreachable |
| 3 | YYYY-MM-DD | <id> | online | <case> | false | <ms> | timeout_error | timeout_s exceeded |
| 4 | YYYY-MM-DD | <id> | online | <case> | false | <ms> | quality_error | quality gate failed |
```
````

### 3.3 新增文件：`docs/fallback-guidelines.md`

````markdown
# Fallback Guidelines

当评测失败时，按顺序执行：

1. `runtime_error`
   - 先检查服务端口/根路径是否可达：`curl http://localhost:8080`
   - 如仓库已提供健康检查端点，再补充：`curl http://localhost:8080/health`
   - 改用离线评测：`python3 eval/run_cases.py --offline`
2. `timeout_error`
   - 降低 `n_predict`，增大 `timeout_s`
3. `quality_error`
   - 调整 prompt / 关键词门控，重新评测
4. `config_error`
   - 修复 `eval/cases.json` 必填字段（`id`, `prompt`）
```
````

### 3.4 运行与生成 JSON 示例命令（与现有入口一致）

```bash
# 1) 离线模式（无需服务）
python3 eval/run_cases.py --offline

# 2) 在线模式（需本地服务）
python3 eval/run_cases.py --server http://localhost:8080

# 3) 从 eval/report.json 提取 trace 样本行（示例）
python3 - <<'PY'
import json, uuid, datetime
r = json.load(open('eval/report.json', 'r', encoding='utf-8'))
for c in r.get('cases', []):
    rid = uuid.uuid4().hex
    total = (c.get('timings_ms') or {}).get('total_ms', c.get('duration_ms', 0.0))
    et = c.get('error_type') or '-'
    print(f"| N | {datetime.date.today()} | {rid} | {r.get('mode')} | {c.get('id')} | {str(c.get('ok')).lower()} | {total} | {et} | imported from eval/report.json |")
PY
```

---

## 4) 本次同步建议的提交说明模板

### Commit message（示例）

- `docs(sync): align career-llm-plan and llm-infer-deploy-lab with vibe observability contract`

### PR 描述（示例）

- 同步了 `request_id/success/timings_ms/error/fallback` 输出约定
- 对齐了 Week2/Week3 错误类型与 trace sample 规范（`invalid_input/repo_not_found/runtime_error/success baseline`）
- 提供了两个目标仓库可直接落地的 README 片段、trace 模板、prompt/guide 模板与可执行命令
