# GPT 真实 API 版说明

这个文档说明项目当前使用的 GPT 真实 function calling 链路。

## 目标

离线 mock 演示已迁移到 `mock/` 子目录；真实入口不再依赖 mock 组件。

## 运行前准备

### 配置模型网关

在 `config.py` 中配置 GPT 兼容网关的 `API_KEY`、`BASE_URL` 和 `MODEL`。

## 运行方式

### 交互模式

```bash
python src/learn_practice/agent/demo_runner.py
```

## 当前实现说明

- `llm_client.py`：封装 GPT 兼容接口调用
- `demo_runner.py`：演示如何把 GPT 的 tool calls 结果交给本地执行器
- `mock/mock_llm.py`：仅供本地离线教学 demo 使用

## 为什么要独立入口

真实入口与离线入口分开后，GPT 调用链路不会误用演示数据。
