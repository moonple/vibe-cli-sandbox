# Performance Compare

本文件整理 `llm-infer-deploy-lab` 中与性能相关的关键结论，用于 `vibe-cli-sandbox` 未来做性能叙事和指标展示。

## 1. 目标

把性能不只当作数字，而是作为产品取舍的一部分：
- 质量 vs 延迟
- 成本 vs 吞吐
- 显存 vs 并发

## 2. 基准结论

### 关键趋势
- `ngl=35` 明显优于 `ngl=20`
- `ctx` 增大后，显存和延迟会增加
- `batch` 的变化会影响吞吐和 TTFT
- 6GB 显存可以支持有限并发，但不能激进

### 代表性结果
- `ctx=2048, ngl=20`：约 22~23 tokens/s
- `ctx=2048, ngl=35`：约 70+ tokens/s
- `ctx=4096, ngl=35`：仍可保持较高吞吐

## 3. 推荐叙事方式

在介绍性能时，建议按下面顺序讲：

1. 环境
2. 配置
3. 指标
4. 结论
5. 取舍

例如：
- 为什么选 `ngl=35`
- 为什么不把 ctx 一味拉大
- 为什么 6GB 显存下要控制并发
- 为什么要在评测中同时记录 TTFT 和 tokens/s

## 4. 建议记录的指标

- `ctx`
- `ngl`
- `batch`
- `tokens/s`
- `TTFT`
- 显存占用
- 并发数
- 模型版本
- 日期

## 5. 对当前仓库的建议

`vibe-cli-sandbox` 后续如果要做性能展示，可以补：
- `results/perf_compare.md`
- `results/dashboard.md`
- `results/trace_samples.md`

这些文件最好和实际 demo、评测结果绑定，而不是只写理论。
