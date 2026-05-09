# Cross-Repo Sync 2026-05

本文件用于把 `career-llm-plan` 与 `llm-infer-deploy-lab` 中与产品1最相关的信息，整理成 `vibe-cli-sandbox` 可直接复用的上下文。

## 1. 来源仓库

- 背景/计划仓库：`moonple/career-llm-plan`
- 推理实验仓库：`moonple/llm-infer-deploy-lab`
- 目标仓库：`moonple/vibe-cli-sandbox`

## 2. 核心定位

### 产品1：Vibe Coding-inspired（开发者工作流）
- 先 CLI，后 FastAPI
- 目标是做出可 demo、可复跑的最小闭环
- 输出重点：`plan` / `patch` / `commands` / `fallback`
- 重点展示：Eval-first、Observability-first、可靠性、回归迭代

### 产品2：Eval + Observability 小平台
- 把产品1沉淀出来的能力平台化
- 重点能力：版本对比、trace 检索、失败聚类、数据集管理

## 3. 需要保留的背景信息

### 个人身份与环境
- 目标角色：AI 产品经理（平台型）
- 环境：Windows 11 + WSL2 + Ubuntu
- GPU：RTX 3060 6GB
- 约束：WSL 内 Hugging Face 访问受限，模型需先下载到 Windows 再拷贝到 WSL

### 已验证推理方向
- llama.cpp（CUDA）
- Qwen2.5-3B-Instruct Q4_K_M GGUF
- 命令行推理与 llama.cpp server

### 评测与观测要求
- 固定用例集（Eval）
- 请求级追踪（Trace）
- TTFT / tokens/s / 错误分类
- 版本对比与回归报告

## 4. 适合直接复用的工作流

### 新对话启动模板
- 复制 `career-llm-plan/prompts/prompt.md` 的内容作为对话首条消息
- 再追加 `plans/weekly-log.md` 的最新一周日志
- 如有必要，再补充 `context/profile.md`、`context/constraints.md` 的相关段落

### 周度维护节奏
- 更新周日志
- 记录新的方向决策 / 常见问答
- 更新环境与约束
- 保持 main 分支为最新

## 5. 文件摘要

### 从 `career-llm-plan` 提取
- `context/profile.md`：AI PM（平台型）定位、产品1/2 描述
- `context/constraints.md`：RTX 3060 6GB、WSL2、Hugging Face 约束
- `context/qa.md`：方向选择、术语、决策记录
- `plans/12-week-plan.md`：12 周交付计划
- `plans/weekly-log.md`：每周复盘模板
- `prompts/prompt.md`：新对话启动提示词
- `projects/llama-cpp-wsl/README.md`：WSL 下 llama.cpp 推理记录

### 从 `llm-infer-deploy-lab` 提取
- `README.md`：推理部署目标、基准测试结论、快速启动方式
- `eval/README.md`：评测脚本、报告结构、错误类型、用例字段

## 6. 最小可复用提示词

> 你好！请先阅读以下背景信息：
> - 我目标是做 AI 产品经理（平台型）
> - 产品1 是 Vibe Coding-inspired 的开发者工作流应用，先 CLI 后 FastAPI
> - 产品2 是 Eval + Observability 小平台
> - 设备是 RTX 3060 6GB，Windows 11 + WSL2 + Ubuntu
> - WSL 内 Hugging Face 访问受限，模型需通过 Windows 下载后拷贝到 WSL
> - 重点是 Eval-first、Observability-first、可靠性、性能与回归迭代
> 请你在后续任务中默认输出：任务拆解、验收标准、风险点、指标建议。

## 7. 建议后续继续补充的内容

- 12 周计划的拆解版
- 周度复盘记录
- 产品 demo 脚本
- 评测 case 集与评分规则
- 性能对比表与 trace 样例
- 最终版启动提示词
