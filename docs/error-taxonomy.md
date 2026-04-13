# Error Taxonomy（Week2）

目标：让失败**可分类、可统计、可回归**，而不是只有一段不稳定的自然语言报错。

本仓库的 `TaskResult.error` 字段在失败时为结构化对象：

- `error.type`：错误类型（枚举，**必须**来自下表）
- `error.message`：人类可读的错误说明（一句话）
- `error.details`：可选的补充上下文（例如异常栈/路径/参数）

---

## 1) 错误类型枚举（Error Type Enum）

> 设计原则：
> 1. `type` 面向系统（统计/聚合/策略）；`message` 面向人（阅读/排查）。
> 2. 枚举数量宁可少但稳定；新增枚举必须更新本文档。
> 3. 同一类原因应归并到同一 `type`，避免“同义不同型”。

### A. 输入/格式类（Input / Format）
| type | 触发条件（When） | 用户下一步（Action / Fallback） |
|---|---|---|
| `invalid_input` | CLI 参数缺失/非法（例如 task 为空、json-out 路径非法等） | 修正参数后重试；运行 `--help` 查看用法 |
| `format_error` | 输出无法解析为 TaskResult，或缺少必需字段（schema 不符合） | 视为 bug：记录 request_id，检查最近改动；必要时回滚 |

### B. 资源/环境类（Resource / Environment）
| type | 触发条件（When） | 用户下一步（Action / Fallback） |
|---|---|---|
| `repo_not_found` | `--repo` 路径不存在/不可访问 | 确认路径；用绝对路径重试 |
| `runtime_error` | 其他未分类异常（IO、权限、依赖缺失等） | 查看 error.details；必要时开启 debug 日志 |

### C. 超时类（Timeout）
| type | 触发条件（When） | 用户下一步（Action / Fallback） |
|---|---|---|
| `timeout_error` | 运行超时（例如单次任务超过 `timeout_s`） | 降低任务复杂度/缩短输出；或提高 timeout |

### D. 语义/质量类（Semantic / Quality）
| type | 触发条件（When） | 用户下一步（Action / Fallback） |
|---|---|---|
| `refusal` | 模型/策略拒绝执行（如果未来接真实 LLM） | 改写 task，或拆成更小步骤 |
| `irrelevant` | 输出与 task 明显不相关（即使运行成功，也可作为质量失败） | 改写 task，或加约束（输出结构/必须包含信息） |

---

## 2) 与 Week2 输出字段的关系

Week2 引入顶层字段：`commands` / `risks` / `fallback`（见 `docs/output-schema.md`）。

约定：
- 即使失败（`success=false`），这三个字段也必须存在（允许为空数组 `[]`）。
- 对于已知错误类型，应尽量在 `fallback` 中给出下一步动作（例如 `repo_not_found` 提示检查路径）。

---

## 3) 示例

### 3.1 repo_not_found（失败示例）

- `success=false`
- `error.type="repo_not_found"`
- `fallback` 给出“检查 repo 路径”的可执行建议

（示例 JSON 省略）
