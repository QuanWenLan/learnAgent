# Function Call 总览

Function call 是模型触发工具调用的一种机制。

在这个学习项目里，它有两种学习方式：

- `mock/mock_llm.py`：模拟模型决定调用哪个函数，适合离线理解原理
- `llm_client.py`：通过 GPT 兼容接口获取 tool calls，适合理解真实项目接法

本地执行部分仍然共用：

- `function_call/functions.py`：定义本地函数
- `function_call/executor.py`：执行函数并返回结果

## 核心理解

function call 更关注一次具体调用：

- 调哪个函数
- 传什么参数
- 返回什么结果

它本身不是完整业务场景，而是 skill 可以使用的一种能力机制。
