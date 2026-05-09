# Career Context Summary

本文件提炼 `career-llm-plan` 中与 `vibe-cli-sandbox` 最相关的背景信息，作为产品1上下文补充。

## 1. 目标与定位

- 目标角色：AI 产品经理（平台型）
- 时间范围：2026-03-21 到 2027-08-31
- 目标：在期限内完成 2 个可展示产品

## 2. 两个产品方向

### 产品1：Vibe Coding-inspired（开发者工作流）
- 形态：先 CLI，后 FastAPI
- 目标：可 demo、可复跑、可量化
- 输出：
  - plan
  - patch / diff
  - commands
  - fallback / recovery
- 核心方法：Eval-first、Observability-first、可靠性、回归迭代

### 产品2：Eval + Observability 小平台
- 目标：把产品1沉淀出来的能力抽象成平台能力
- 重点：
  - 数据集 / 用例管理
  - 版本对比报告
  - trace 检索与失败聚类

## 3. 作品集能力栈

- Eval-first：固定用例集、版本对比、成功率与失败类型分布
- Observability-first：request_id、阶段耗时、token 统计、错误码
- Reliability：超时、取消、重试、降级、并发控制
- Cost/Latency：ctx / batch / 并发与性能取舍
- Release/Regression：每次改动都要有回归结果

## 4. 常见结论

- 产品1 先做 CLI，再升级 FastAPI 是合理路线
- 产品1 先用 Mock 后端，优先做产品体验与闭环
- 产品1 不追求 IDE 级自动写代码，先做最小闭环
- 产品1 和产品2 的边界：
  - 产品1 面向用户任务闭环
  - 产品2 面向质量体系与平台化

## 5. 可直接复用的对话要求

后续对话默认输出：
1. 任务拆解（1-2 天粒度）
2. 验收标准（可量化）
3. 风险点与备选方案
4. 指标建议（Eval / Trace / 性能 / 可靠性）
