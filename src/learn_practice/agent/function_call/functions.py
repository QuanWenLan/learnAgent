"""真实 function call 的具体实现。"""
from urllib.parse import quote

def get_weather(city: str) -> dict:
    """查询真实天气（wttr.in，免费无需 key）。"""
    import requests

    try:
        resp = requests.get(
            f"https://wttr.in/{quote(city)}",
            params={"format": "j1", "lang": "zh"},
            timeout=10,
        )
        resp.raise_for_status()
        cur = resp.json()["current_condition"][0]
        desc = (cur.get("lang_zh") or cur["weatherDesc"])[0]["value"]
        return {
            "city": city,
            "weather": desc,
            "temperature": cur["temp_C"],
            "advice": "数据来源：wttr.in 实时接口",
        }
    except Exception as e:
        return {"city": city, "weather": "未知", "temperature": "未知", "advice": f"实时接口不可用：{e}"}


def query_order(order_id: str) -> dict:
    """查询订单状态；当前项目未配置真实订单后端。"""
    return {
        "order_id": order_id,
        "status": "未配置真实订单系统",
        "logistics": "暂无",
        "eta": "当前仅支持 mock 演示数据。"
    }


_BING_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def search_docs(keyword: str, max_results: int = 3) -> list:
    """用必应搜索真实资料，返回 [{title, summary, link}]。"""
    import requests
    from bs4 import BeautifulSoup

    try:
        max_results = int(max_results)
    except (TypeError, ValueError):
        max_results = 3
    try:
        resp = requests.get(
            "https://cn.bing.com/search",
            params={"q": keyword},
            headers=_BING_HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for li in soup.select("li.b_algo"):
            a = li.select_one("h2 a")
            if not a:
                continue
            p = li.select_one(".b_caption p") or li.select_one("p")
            results.append({
                "title": a.get_text(strip=True),
                "summary": p.get_text(strip=True) if p else "",
                "link": a.get("href", ""),
            })
            if len(results) >= max_results:
                break
        if results:
            return results
    except Exception:
        pass
    return []
