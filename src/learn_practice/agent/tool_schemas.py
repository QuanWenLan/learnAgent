"""生产链路共用的工具定义。"""

FUNCTION_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "根据城市名称查询天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "query_order",
        "description": "根据订单号查询订单状态",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "订单编号"}
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "search_docs",
        "description": "根据关键词搜索文档",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "文档关键词"}
            },
            "required": ["keyword"]
        }
    }
]
