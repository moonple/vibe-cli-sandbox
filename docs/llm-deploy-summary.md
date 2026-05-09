# LLM Deploy Summary

本文件提炼 `llm-infer-deploy-lab/README.md` 中与 `vibe-cli-sandbox` 最相关的信息，主要保留推理部署、性能、评测三个部分。

## 1. 项目目标

- 掌握 LLM 推理部署工程化能力
- 构建可观测、可扩展的推理服务
- 为求职积累可量化的项目经验

## 2. 环境配置

- 系统：Windows 11 + WSL2 (Ubuntu)
- GPU：NVIDIA RTX 3060 6GB
- 框架：llama.cpp (CUDA)
- 模型：Qwen2.5-3B-Instruct-Q4_K_M (GGUF)

## 3. 关键基准结论

### 性能趋势
- `ngl=35` 明显优于 `ngl=20`
- `ctx=4096, ngl=35, batch=256` 是当前最优组合之一
- 6GB 显存可支持约 2 个并发 slot，但需要关注显存余量

### 代表性结果
- `ctx=2048, ngl=20`：约 22~23 tokens/s
- `ctx=2048, ngl=35`：约 70+ tokens/s
- `ctx=4096, ngl=35`：仍能保持 60~70+ tokens/s

## 4. 快速启动要点

- 使用 `./scripts/run_server.sh` 启动服务
- 使用 `curl http://localhost:8080/completion` 做快速验证
- 将评测模式分为：
  - 离线模式：仅校验 test case schema
  - 在线模式：需要本地服务已启动

## 5. Eval 结构化信息

### 评测输出
- `eval/report.json`
- `eval/report.md`

### 错误类型
- `runtime_error`：HTTP / 网络错误
- `timeout_error`：请求超时
- `quality_error`：服务正常但未满足质量门控
- `config_error`：test case 缺少必填字段

### 用例字段
- `id`
- `prompt`
- `n_predict`
- `temperature`
- `timeout_s`
- `expect_min_len`
- `expect_contains`

## 6. 对当前仓库的启发

`vibe-cli-sandbox` 后续也应该保留类似的结构：
- 可重复运行的评测入口
- 明确的错误分类
- 结构化报告输出
- 便于对比版本的指标记录
