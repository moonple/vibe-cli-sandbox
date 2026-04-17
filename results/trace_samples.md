# Trace Samples (Week3)

> 目的：提供可复现的 trace 样本，证明每次运行可追踪 request_id、耗时、失败类型与 fallback。

| # | date | request_id | task | repo | success | total_ms | error.type | notes |
|---:|---|---|---|---|---|---:|---|---|
| 1 | 2026-04-17 | b189127cfda744da85cf28ac404dcea0 | timing smoke test | . | true | 0.08671300020068884 |  | success baseline |
| 2 | 2026-04-17 | 4cd8c85083164ce09dfeb4f586a2a487 | (empty / spaces) | . | false |  0.0 | invalid_input | pre-check in CLI |
| 3 | 2026-04-17 | 9fafb0a6929f4fc193a5a172f2527a97 | test | /path/does/not/exist | false | 0.038772999914726824 | repo_not_found | validation in runner |
| 4 | 2026-04-17 | 8abb7707679a45359a4ecc4bfbfd1a62 | timing smoke test | . | false | 0.0 | runtime_error | failed writing --json-out /root/out.runtime.json (Permission denied), wrote fallback out.error.json |
| 5 | 2026-04-17 | 527e1215e4e44eab935c6e7f7cb79582 | "   " | . | false | 0.0 | invalid_input | task is whitespace-only |
