"""离线 function call 实现，使用固定演示数据。"""

from .fake_data import DOC_DATA, ORDER_DATA, WEATHER_DATA


def get_weather(city: str) -> dict:
    data = WEATHER_DATA.get(city, WEATHER_DATA["北京"])
    return {
        "city": city,
        "weather": data["weather"],
        "temperature": data["temperature"],
        "advice": data["advice"]
    }


def query_order(order_id: str) -> dict:
    order = ORDER_DATA.get(order_id)
    if order is None:
        return {
            "order_id": order_id,
            "status": "未找到",
            "logistics": "暂无",
            "eta": "请检查订单号是否正确。"
        }
    return {
        "order_id": order_id,
        "status": order["status"],
        "logistics": order["logistics"],
        "eta": order["eta"]
    }


def search_docs(keyword: str, max_results: int = 3) -> list:
    del keyword
    return DOC_DATA[:max_results]


FUNCTION_REGISTRY = {
    "get_weather": get_weather,
    "query_order": query_order,
    "search_docs": search_docs
}
