# MCP 总览

MCP 可以理解为一种统一外部工具接入的方式。

在这个学习项目里，MCP 相关文件包括：

- `mcp/tools.py`
- `mock/mcp/fake_mcp_server.py`（仅离线演示）
- `mcp/mcp_client.py`

## 核心理解

MCP 主要解决的是：

- 外部工具如何标准化接入
- Agent 如何用统一方式调用不同工具

## 和 function call 的区别

- function call 更像本地工具调用机制
- MCP 更像外部工具接入协议层
