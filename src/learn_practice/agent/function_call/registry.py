try:
    from .functions import get_weather, query_order, search_docs
except ImportError:
    from function_call.functions import get_weather, query_order, search_docs


FUNCTION_REGISTRY = {
    "get_weather": get_weather,
    "query_order": query_order,
    "search_docs": search_docs
}
