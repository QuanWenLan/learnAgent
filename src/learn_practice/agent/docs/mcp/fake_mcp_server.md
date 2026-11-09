# Fake MCP Server 说明

这个项目里的 `mock/mcp/fake_mcp_server.py` 不是完整 MCP 协议实现，而是一个仅供离线教学使用的简化版本。

## 当前模拟的工具

- `kb.search`
- `doc.search`

## 目的

帮助你理解：

1. skill 可以不直接调用本地函数
2. skill 也可以通过统一 client 去调外部工具
3. MCP 的价值在于标准化接入，而不是把工具硬编码进每个 skill
