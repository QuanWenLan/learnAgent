# 架构说明

这个学习项目的目标不是实现一个复杂框架，而是把最常见的 Agent 工程分层压缩成一个可以直接阅读和运行的最小样板。

## 分层结构

```text
用户输入
  -> IntentRouter
      -> Skill
          -> Function Call / MCP
              -> Tool Result
                  -> Skill 汇总
                      -> Agent 输出
```

## 关键模块

- `main.py`：主入口，串起完整流程
- `router.py`：意图识别
- `skills/`：按任务封装 skill
- `function_call/`：本地工具调用机制
- `mcp/`：外部工具接入客户端
- `tool_schemas.py`：真实与 mock 共用的 function schema
- `mock/`：离线模型、演示数据和 fake MCP 组件

## 设计重点

### 1. 为什么把意图识别和 function call 拆开

因为两者职责不同：

- 意图识别：决定去哪一个 skill
- function call：决定具体调哪一个函数

### 2. 为什么 skill 单独成层

因为真实项目里，一个任务通常不止一步。skill 层更接近业务能力编排。

### 3. 为什么还要有 MCP

因为真实项目的很多能力不是本地函数，而是外部系统工具。MCP 层有助于你理解标准化接入思路。
