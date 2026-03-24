# Output Schema

本仓库的核心输出为 `TaskResult`，既用于 Demo 展示，也用于 Eval 回归。

## 1) TaskResult (out.json 顶层对象)

| Field | Type | Required | 描述 |
|---|---|---:|---|
| request_id | string | yes | 本次运行唯一标识（建议用于 trace/eval 关联） |
| success | boolean | yes | 是否成功 |
| message | string | no | 简要信息/总结 |
| timings_ms | object(string -> number) | yes | 耗时统计（毫秒）。至少包含 `total_ms` |
| error | object \| null | no | 失败时的结构化错误信息（见 ErrorInfo），成功时为 `null` |
| plan | array(string) | yes | 计划步骤列表（可为空；用于质量门槛/回归） |
| changes | array(Change) | yes | 变更列表（见 Change），可为空 |

### timings_ms 约定
- `total_ms`：端到端总耗时（必须）
- 可选阶段字段（示例）：`validate_repo_ms`、`mock_generate_ms`、`serialize_ms` 等

## 2) Change

| Field | Type | Required | 描述 |
|---|---|---:|---|
| file | string | yes | 文件路径/文件名 |
| summary | string | yes | 对变更的简述 |
| diff | string \| null | no | diff/patch（可选，当前可为 mock） |

## 3) ErrorInfo

| Field | Type | Required | 描述 |
|---|---|---:|---|
| type | string | yes | 错误类型（例如 `repo_not_found`） |
| message | string | yes | 错误信息 |
| details | string \| null | no | 额外上下文（可选） |

## 4) 成功示例 (out.json)

```json
{
  "request_id": "4875e746549b41908d76b0350d3cf0ea",
  "success": true,
  "message": "Successfully processed task: timing smoke test",
  "timings_ms": {
    "validate_repo_ms": 0.02,
    "mock_generate_ms": 0.03,
    "total_ms": 0.07
  },
  "error": null,
  "plan": [
    "1. Scan repository structure and identify relevant files",
    "2. Propose minimal changes as a patch/diff",
    "3. Provide verification commands and fallback guidance"
  ],
  "changes": [
    {
      "file": "README.md",
      "summary": "Updated documentation with task information",
      "diff": "+ # Task: timing smoke test\n+ This task was processed by vibe."
    }
  ]
}
```

## 5) 失败示例 (out.json)

```json
{
  "request_id": "4279ecbff61744a0bfe47507ae932e20",
  "success": false,
  "message": "Repository path not found: __repo_does_not_exist__",
  "changes": [],
  "plan": [],
  "timings_ms": {
    "validate_repo_ms": 0.0918,
    "total_ms": 0.1087
  },
  "error": {
    "type": "repo_not_found",
    "message": "Repository path not found: __repo_does_not_exist__",
    "details": null
  }
}
```

## 6) 字段存在性说明

根据当前实现（vibe-cli-sandbox v0.1.0）：
- `plan` 字段**始终存在**：成功时至少包含 3 条默认步骤，失败时为空数组 `[]`
- `changes` 字段**始终存在**：成功时有模拟变更，失败时为空数组 `[]`
- `error` 字段：失败时为结构化对象，成功时为 `null`
- 这种设计确保了输出格式的一致性，便于评测脚本统一处理
