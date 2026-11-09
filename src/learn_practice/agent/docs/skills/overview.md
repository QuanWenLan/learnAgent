# Skill 总览

Skill 是面向某类任务的能力封装。

在这个项目里，一共有 4 个 skill：

- `weather_skill.py`
- `order_skill.py`
- `research_skill.py`
- `chat_skill.py`

同时，这个项目也演示了另一种更贴近真实工程的设计：

- `docs/skills/*.md` 不只是文档
- 它们也可以被解析成 skill 配置
- skill 的 prompt 正文可以直接提供给模型
- `mock/markdown_skill_runtime.py` 可以根据这些配置直接驱动离线演示链路

## Skill 的职责

一个 skill 通常负责：

1. 接收已经分流后的请求
2. 决定内部执行步骤
3. 按需调用 function call 或 MCP
4. 整理结果并输出

## 为什么要把 skill 单独拆开

因为它比 function 更高一层，更接近业务场景。

比如“查询天气”并不只是一个函数名，而是一整个场景能力：

- 理解输入
- 提取参数
- 调用工具
- 组织答案

这就是 skill 的价值。
