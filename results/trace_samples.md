# Trace Samples (Week3)

> 目的：提供可复现的 trace 样本，证明每次运行可追踪 request_id、耗时、失败类型与 fallback。

| # | date | request_id | task | repo | success | total_ms | error.type | notes |
|---:|---|---|---|---|---|---:|---|---|
| 1 | 2026-04-17 | (paste) | timing smoke test | . | true | (paste) |  | success baseline |
| 2 | 2026-04-17 | (paste) | (empty / spaces) | . | false | (paste) | invalid_input | pre-check in CLI |
| 3 | 2026-04-17 | (paste) | test | /path/does/not/exist | false | (paste) | repo_not_found | validation in runner |
| 4 | 2026-04-17 | (paste) | (your choice) | . | false | (paste) | runtime_error | force an exception |
| 5 | 2026-04-17 | (paste) | (your choice) | . | true/false | (paste) |  | additional sample |
