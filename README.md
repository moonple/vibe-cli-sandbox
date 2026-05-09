# vibe-cli-sandbox

这是一个用于沉淀 LLM 推理部署、Eval、Observability 和 Vibe Coding-inspired 开发者工作流的实验仓库。

## 仓库目标

本仓库主要用于：

- 记录产品1：Vibe Coding-inspired 的开发者工作流
- 沉淀 Eval-first、Observability-first 的实现思路
- 保留推理部署、性能基准和评测经验
- 为后续 CLI -> FastAPI 演进提供上下文
- 作为新对话的启动上下文仓

## 快速使用

如果你想快速恢复项目背景，建议先阅读：

- `docs/startup-prompt.md`
- `docs/career-context-summary.md`
- `docs/career-plan-summary.md`
- `docs/llm-deploy-summary.md`
- `docs/environment-constraints.md`

如果你想了解具体的工程原则与评测方式，再看：

- `docs/reliability.md`
- `docs/perf-compare.md`
- `docs/eval-spec.md`

如果你想追踪这些文档从哪里来，可以看：

- `docs/source-index.md`

## 项目文档入口

- `docs/startup-prompt.md`  
  新对话启动提示词，适合直接复制给 Copilot / LLM。

- `docs/career-context-summary.md`  
  记录项目目标、产品1/产品2 定位、背景与约束。

- `docs/career-plan-summary.md`  
  记录 12 周计划、阶段路线图与最终验收标准。

- `docs/llm-deploy-summary.md`  
  记录推理部署环境、基准测试结论与 Eval 经验。

- `docs/environment-constraints.md`  
  记录硬件、WSL2、Hugging Face、显存等环境限制。

- `docs/reliability.md`  
  记录超时、取消、降级、重试、并发控制等可靠性策略。

- `docs/perf-compare.md`  
  记录性能基准、ctx / ngl / batch 取舍与指标叙事。

- `docs/eval-spec.md`  
  记录评测模式、错误分类、用例字段与报告结构。

- `docs/source-index.md`  
  记录这些文档的来源仓库与同步原则。

## 推荐阅读顺序

1. `docs/startup-prompt.md`
2. `docs/career-context-summary.md`
3. `docs/career-plan-summary.md`
4. `docs/environment-constraints.md`
5. `docs/llm-deploy-summary.md`
6. `docs/reliability.md`
7. `docs/perf-compare.md`
8. `docs/eval-spec.md`

## 使用建议

1. 先用 `docs/startup-prompt.md` 恢复对话上下文
2. 再根据需要查看对应的摘要文档
3. 如果要做 demo，优先参考：
   - 任务拆解
   - 输出结构
   - 评测规范
   - 可靠性策略
4. 如果要做性能说明，参考：
   - `docs/perf-compare.md`
   - `docs/llm-deploy-summary.md`
5. 如果要做回归与质量控制，参考：
   - `docs/eval-spec.md`
   - `docs/reliability.md`

## 同步原则

本仓库中的文档主要采用以下原则：

- 以摘要化 + 可执行化 + 可复用为主
- 不整仓搬运原始材料
- 保留关键结论、命令、指标、提示词和边界说明
- 所有新增内容都尽量服务于产品1的 demo、评测和回归

## 来源仓库

- `moonple/career-llm-plan`
- `moonple/llm-infer-deploy-lab`
