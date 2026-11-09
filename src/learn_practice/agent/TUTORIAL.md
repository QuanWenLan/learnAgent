# 简单 Agent 学习教程

> 这个教程通过一个最小可运行工程，帮助你理解一个简单自研 Agent 在正常情况下是如何组织起来的。

## 1. 先看整体目标

这个学习项目不是为了追求真实生产强度，而是为了把几个关键概念拆开讲清楚：

- Agent 主循环
- 意图识别
- skill 路由
- function call
- MCP 调用

你可以把这个项目看成是市场上很多 Agent 工程的“缩小版教学模型”。

## 2. 一个简单 Agent 往往有哪些层

一个常见的简化分层如下：

```text
用户输入
  -> 意图识别
      -> 选择 skill
          -> 决定是否调用工具
              -> function call 或 MCP
                  -> 返回结果
                      -> skill 汇总答案
                          -> 输出给用户
```

## 3. 什么是意图识别

意图识别解决的是：**用户这句话到底想做什么**。

比如：

- “北京天气怎么样” -> 天气意图
- “查一下订单 A1001” -> 订单意图
- “帮我搜索 agent 资料” -> 资料检索意图
- 其他 -> 闲聊意图

在这个项目里，`router.py` 用的是最简单的关键词规则匹配。

市场上常见演进路线通常是：

1. 规则匹配
2. 分类模型 / embedding 检索
3. LLM router

## 4. 什么是 skill

skill 是面向某一类任务的能力封装。

例如：

- `weather_skill.py` 负责天气场景
- `order_skill.py` 负责订单场景
- `research_skill.py` 负责资料检索场景
- `chat_skill.py` 负责兜底闲聊

skill 不只是一个函数，它往往还会负责：

- 组织执行步骤
- 调用工具
- 汇总结果
- 输出最终回答

## 5. function call 和 skill 有什么区别

这是这个项目重点解释的一部分。

### function call

function call 更像一种**工具调用机制**。

它主要关心：

- 工具叫什么名字
- 参数是什么结构
- 模型如何选择它
- 程序如何执行它

在这个项目里：

- `mock/mock_llm.py` 模拟“模型选择函数”（离线入口）
- `function_call/functions.py` 定义本地函数
- `function_call/executor.py` 负责执行

### skill

skill 更像一种**任务能力封装和编排层**。

它主要关心：

- 当前场景是什么
- 需要走什么步骤
- 是否要调工具
- 最终怎么组织结果

### 二者关系

如果 skill 里包含工具调用，那么它们不是二选一，而是分层关系：

- skill 负责“做什么、如何编排”
- function call 负责“具体怎么调工具”

## 6. 什么是 MCP

MCP 可以理解为一种统一外部工具接入的思路。

它解决的是：

- 外部工具很多，接法不统一
- Agent 不应该和每个系统都强耦合
- 需要一种标准方式去调用工具

在这个学习项目里：

- `mock/mcp/fake_mcp_server.py` 模拟 MCP server（离线入口）
- `mcp/mcp_client.py` 模拟 MCP client
- `research_skill.py` 演示如何通过 MCP 查询资料

这里没有完整复刻真实 MCP 协议，而是保留了最核心的理解目标：

**把外部工具标准化接入 Agent。**

## 7. 这个项目里的三种典型场景

### 场景 1：天气查询

```text
用户提问
  -> router 识别为 weather
      -> weather skill
          -> mock LLM 选择 get_weather
              -> function executor 执行
                  -> 返回天气结果
```

### 场景 2：订单查询

```text
用户提问
  -> router 识别为 order
      -> order skill
          -> mock LLM 选择 query_order
              -> function executor 执行
                  -> 返回订单结果
```

### 场景 3：资料检索

```text
用户提问
  -> router 识别为 research
      -> research skill
          -> 构造 MCP tool call
              -> MCP client 调用 fake MCP server
                  -> 返回资料结果
```

## 8. 为什么这里还要加一个 mock LLM

因为很多人第一次看 Agent 工程时，容易把“路由”和“function call”混在一起。

这里故意拆开：

- `router.py` 负责识别意图
- `mock/mock_llm.py` 负责模拟 function call 选择

这样你可以看清楚：

- 前者是“应该走哪个 skill”
- 后者是“在 skill 内部具体调哪个函数”

## 9. 市场上常见实现方式

### 方式一：只有 function call

- 给模型注册很多 tools
- 模型自行决定调用哪个
- 适合小 demo

### 方式二：intent router + skill + function call

- 先做路由
- 再进入 skill
- 再由 skill 调 function
- 更适合业务型项目

### 方式三：intent router + skill + MCP + function call

- skill 负责场景编排
- function call 负责本地工具调用
- MCP 负责外部工具接入
- 更接近平台化 Agent 工程

## 10. Skill 可以做成配置吗

可以，而且这正是很多 Agent 工程里很常见的做法。

在这个项目里，`docs/skills/*.md` 现在已经不仅仅是说明文档，还可以作为 skill 配置来源。

每个 skill Markdown 现在包含：

1. front matter 元数据
   - `name`
   - `description`
   - `intent`
   - `tools`
   - `input_hint`
2. prompt 正文
   - 这部分内容可以直接给模型

例如一个 skill 文件可以同时承担两个角色：

- 给人看：解释这个 skill 做什么
- 给模型看：作为提示词或能力说明

这也是为什么很多平台化 Agent 系统会把 skill 定义做成：

- Markdown
- YAML
- JSON
- 数据库存储的 prompt 配置

在本项目里，对应实现是：

- `skill_config.py`：解析 skill markdown
- `skill_config_demo.py`：演示如何读取 skill 配置
- `docs/skills/*.md`：实际的 skill 配置文件
- `docs/skills/overview.md`：仅作为人工阅读总览，不参与解析
- `mock/markdown_skill_runtime.py`：基于 Markdown 配置执行离线 skill
- `mock/markdown_agent_demo.py`：演示 Markdown skill runtime 的完整离线链路

## 11. 如何运行

### 固定演示

```bash
python src/learn_practice/agent/demo_runner.py
```

### 交互演示

```bash
python src/learn_practice/agent/main.py
```

### 真实 API function calling 演示

```bash
python src/learn_practice/agent/demo_runner.py
```

### Markdown skill runtime 演示

```bash
python src/learn_practice/agent/mock/markdown_agent_demo.py
```

你可以试着输入：

- `北京今天天气怎么样？`
- `帮我查一下订单 A1002`
- `帮我搜索一下 mcp 相关资料`
- `你好，介绍一下自己`

真实 GPT 调用使用 `config.py` 中的兼容网关配置，具体说明见 `docs/function_call/real_api.md`。

## 11. 接下来可以怎么扩展

如果你后续想继续深入，可以继续加：

1. 真正的 function schema JSON 细化
2. HTTP 版 fake MCP server
3. 多轮会话记忆
4. 更复杂的 skill 编排
5. Agent 输出 trace / 日志
6. LLM router 替换规则路由

## 12. 推荐阅读顺序

1. `README.md`
2. `docs/architecture.md`
3. `docs/intent_router/overview.md`
4. `docs/skills/overview.md`
5. `docs/function_call/overview.md`
6. `docs/mcp/overview.md`
7. 运行 `demo_runner.py`
8. 阅读 `docs/function_call/real_api.md`
9. 对照源码逐步阅读
