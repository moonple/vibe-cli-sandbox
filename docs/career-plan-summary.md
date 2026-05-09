# Career Plan Summary

本文件提炼 `career-llm-plan/plans` 中最值得保留到 `vibe-cli-sandbox` 的计划内容。

## 1. 总体目标

- 周期：2026-03-23 ~ 2026-06-14
- 定位：开发者场景 AI 应用，但重点展示平台能力
- 主线：Eval-first + Observability-first + 回归迭代

## 2. 最终验收

到 2026-06-14，至少完成：
- 一个可演示 demo：输入任务 → 输出方案/patch → 本地验证 → 生成报告
- Trace：每次请求可追踪阶段耗时与错误
- Eval：至少 30 条任务用例集 + 回归对比报告
- README：别人按步骤可以跑通，并看到指标

## 3. 阶段路线图

### Week 1
- 定义用户故事
- 定义最小输入/输出格式
- 跑通端到端 demo

### Week 2
- 输出结构化
- 定义失败类型

### Week 3
- 增加 request_id
- 记录阶段耗时与 token 统计
- 失败原因写日志

### Week 4
- 设计 30 条 coding 用例
- 建立评测与基线报告

### Week 5
- 统计失败 Top3
- 调整 prompt/策略
- 输出 v0 vs v1 对比

### Week 6
- 超时 / 取消 / 降级
- 失败时给出可执行下一步

### Week 7
- 固化性能采集
- 做配置对比与取舍结论

### Week 8
- 汇总核心指标表
- 固化报告模板

### Week 9
- 扩充用例集到 60~100
- 引入版本标签与回归流程

### Week 10
- 写产品故事与 PM 叙事文档

### Week 11
- 最终 Demo
- README 打磨

### Week 12
- 产品复盘
- 启动产品2 PRD

## 4. 关键产物方向

适合继续保留在 `vibe-cli-sandbox` 的内容：
- `docs/demo-script.md`
- `docs/output-schema.md`
- `docs/error-taxonomy.md`
- `docs/observability.md`
- `docs/reliability.md`
- `results/perf_compare.md`
- `results/dashboard.md`
- `docs/product-story.md`
- `docs/postmortem.md`
- `docs/prd-product2.md`

## 5. 这份计划对当前仓库的意义

它说明 `vibe-cli-sandbox` 不只是一个 CLI demo，而是一个可以逐步演化成：
- 有结构化输出的产品
- 有可观测数据的产品
- 有评测与回归能力的产品
