# Environment Constraints

本文件整理 `career-llm-plan` 与 `llm-infer-deploy-lab` 中与当前开发环境相关的约束信息，方便 `vibe-cli-sandbox` 在实现与演示时保持一致。

## 1. 硬件环境

- GPU：NVIDIA RTX 3060（6 GB 显存）
- 系统：Windows 11 + WSL2（Ubuntu）
- 主语言：Python（优先）
- 版本控制：Git + GitHub

## 2. 已验证推理环境

- 框架：llama.cpp（CUDA 编译版）
- 模型：Qwen2.5-3B Instruct，Q4_K_M GGUF
- 推理方式：命令行或 llama.cpp 自带 server
- 显存占用：约 3–4 GB（Q4_K_M，ctx=2048，具体以实测为准）

## 3. 网络与下载约束

### Hugging Face 访问问题
WSL2 内无法稳定直连 Hugging Face，推荐工作流：

1. 在 Windows 浏览器或工具中下载 GGUF 模型文件
2. 将模型文件拷贝到 WSL 本地目录
3. 在 WSL 内加载模型进行推理

### 常用镜像站
- `https://hf-mirror.com`

## 4. 文件系统约束

- 模型文件不要放在 `/mnt/c/` 下
- 建议放在 WSL 本地路径，例如 `/home/<user>/models/`
- 原因：WSL2 下 Windows 挂载路径 I/O 性能较差

## 5. 显存约束

- 6 GB 显存限制了可运行模型规模
- Q4_K_M 的 3B 模型可用
- 7B Q4_K_M 勉强可用，但需降低 ctx
- 13B 及以上通常不适合直接运行

### 上下文长度建议
- 日常测试：`ctx = 2048`
- 最大可用：`ctx = 4096`（需实测）

## 6. 性能与并发约束

- `ngl` 对性能影响很大
- `ngl=35` 显著优于 `ngl=20`
- 并发数不能过高，6GB 显存下建议保守处理
- 需要同时记录 TTFT、tokens/s 与显存占用

## 7. 开发与实验建议

- 优先使用 CLI 验证核心闭环
- 真正接模型前，可先使用 mock backend 保证流程跑通
- 需要保留：
  - 失败类型
  - 恢复路径
  - 评测报告
  - 性能对比结果

## 8. 对当前仓库的意义

这些约束决定了 `vibe-cli-sandbox` 的设计应该偏向：
- 轻量
- 可复跑
- 可观测
- 可评测
- 资源友好
