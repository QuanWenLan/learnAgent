# Agent 学习项目

> 一个用于理解自研简单 Agent 工程的最小学习样板，包含意图识别、skill 调用、function call 和 MCP 调用。

## 项目目标

这个目录提供真实调用链路，并将离线 mock 教学流程集中在 `mock/` 子目录，帮助理解：

- 什么是意图识别
- 什么是 skill
- 什么是 function call
- 什么是 MCP
- skill、function call、MCP 之间如何协作
- 如何在保留本地 demo 的同时接入真实 API

## 目录结构

```text
agent/
├── __init__.py
├── bootstrap.py
├── README.md
├── TUTORIAL.md
├── main.py
├── demo_runner.py
├── router.py
├── tool_schemas.py
├── schemas.py
├── docs/
│   ├── architecture.md
│   ├── skills/
│   │   ├── overview.md
│   │   ├── weather_skill.md
│   │   ├── order_skill.md
│   │   └── research_skill.md
│   ├── function_call/
│   │   ├── overview.md
│   │   ├── examples.md
│   │   └── real_api.md
│   ├── mcp/
│   │   ├── overview.md
│   │   └── fake_mcp_server.md
│   └── intent_router/
│       ├── overview.md
│       └── examples.md
├── function_call/
├── mcp/
├── skills/
└── mock/
    ├── demo_runner.py
    ├── markdown_agent_demo.py
    ├── markdown_skill_runtime.py
    ├── mock_llm.py
    ├── fake_data.py
    ├── functions.py
    └── mcp/fake_mcp_server.py
```

## 快速开始

### 运行固定演示

```bash
python src/learn_practice/agent/demo_runner.py
```

### 运行交互模式

```bash
python src/learn_practice/agent/main.py
```

### 运行真实模型链路（默认：LLM 意图路由 + 真实工具数据 + 结果回填生成回答）

```bash
python src/learn_practice/agent/demo_runner.py          # 固定演示
python src/learn_practice/agent/main.py                 # 交互模式
```

### 运行离线 mock 演示

```bash
python src/learn_practice/agent/mock/demo_runner.py
python src/learn_practice/agent/mock/markdown_agent_demo.py
```

## Skill 配置化

这个项目现在支持把 skill 文档写成“可加载配置”的 Markdown：

- `docs/skills/weather_skill.md`
- `docs/skills/order_skill.md`
- `docs/skills/research_skill.md`
- `docs/skills/chat_skill.md`

这些文件包含两部分：

1. front matter 元数据
2. 提供给模型的 prompt 正文

注意：`docs/skills/overview.md` 是给人阅读的总览，不参与 skill 配置解析。

你可以通过下面的命令查看解析结果：

```bash
python src/learn_practice/agent/skill_config_demo.py
```

这意味着 `skill.md` 不只是说明文档，也可以直接作为模型可读的 skill 配置来源。

同时，项目里新增了一个独立运行链路：

- `mock/markdown_skill_runtime.py`
- `mock/markdown_agent_demo.py`

这条链路会：

1. 识别意图
2. 加载对应的 `skill.md`
3. 读取其中的工具配置和 prompt 正文
4. 再执行工具并返回结果

## 推荐学习顺序

1. 先看 `TUTORIAL.md`
2. 再看 `docs/architecture.md`
3. 运行 `demo_runner.py` 看真实整体链路，或运行 `mock/demo_runner.py` 看离线链路
4. 阅读 `router.py` 理解意图识别
5. 阅读 `skills/` 理解 skill 封装
6. 阅读 `function_call/` 理解 function call 执行机制
7. 阅读 `mcp/` 理解 MCP 接入方式
8. 最后阅读 `llm_client.py`，理解 GPT 兼容接口调用和结果回填

## 演示场景

- 天气查询：意图识别 → weather skill → function call
- 订单查询：意图识别 → order skill → function call
- 资料搜索：意图识别 → research skill → MCP 调用
- 闲聊兜底：意图识别 → chat skill
- 真实模型调用：OpenAI 兼容网关 → tool_calls → 本地执行器 → 结果回填生成回答
- 订单查询：当前没有真实订单系统，仅在 mock 入口提供演示数据
