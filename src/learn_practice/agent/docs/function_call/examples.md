# Function Call 示例

## 示例 1：天气查询

```text
输入：北京今天天气怎么样？
mock LLM 输出：get_weather(city="北京")
执行结果：返回北京天气数据
```

## 示例 2：订单查询

```text
输入：帮我查一下订单 A1001
mock LLM 输出：query_order(order_id="A1001")
执行结果：返回订单状态
```

## 学习重点

- function call 不是 skill
- function call 是 skill 内部可使用的一种执行机制
- 真实大模型产品里，模型通常会根据函数 schema 自动选择调用
