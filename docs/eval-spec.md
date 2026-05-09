# Eval Spec

本文件整理评测系统规范，参考 `llm-infer-deploy-lab/eval/README.md`，用于 `vibe-cli-sandbox` 未来搭建自己的评测与回归机制。

## 1. 目标

建立一套可重复运行、可对比、可回归的评测机制。

## 2. 运行模式

### 离线模式
- 不依赖本地服务
- 主要校验 test case schema
- 适合 CI 默认执行

### 在线模式
- 需要本地服务已启动
- 用于真实性能和质量验证
- 适合本地回归和 demo 前检查

## 3. 输出文件

- `eval/report.json`
- `eval/report.md`

## 4. 错误类型

### runtime_error
HTTP 或网络错误

### timeout_error
请求超时

### quality_error
服务正常响应，但不满足质量门控

### config_error
test case 缺少必填字段

## 5. 用例字段

- `id`：用例标识
- `prompt`：输入提示词
- `n_predict`：最大生成 token 数
- `temperature`：温度参数
- `timeout_s`：超时秒数
- `expect_min_len`：响应最短长度
- `expect_contains`：必须包含的关键词

## 6. 推荐的质量门控

- 输出不能为空
- 输出长度不能过短
- 必须包含指定关键字
- 结构必须符合 schema
- 超时算失败

## 7. 推荐评测流程

1. 准备用例集
2. 跑离线 schema 校验
3. 启动本地服务
4. 跑在线评测
5. 生成 report
6. 记录对比结果
7. 根据失败类型修复

## 8. 对当前仓库的建议

如果 `vibe-cli-sandbox` 后续要增强评测能力，建议增加：
- `eval/cases_v0.json`
- `eval/run_cases.py`
- `eval/report.json`
- `eval/report.md`

并把失败类型和报告结构固定下来，便于版本对比和回归。
