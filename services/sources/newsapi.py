import requests
from datetime import datetime, timedelta, timezone
from config import NEWSAPI_KEY, MAX_ARTICLES_PER_TOPIC

NEWSAPI_URL = "https://newsapi.org/v2/everything"


def _build_query(topic: str) -> str:
    topic = topic.strip()
    if " " in topic:
        return f'"{topic}"'
    return topic


def fetch(topic: str, max_results: int = MAX_ARTICLES_PER_TOPIC) -> list:
    if not NEWSAPI_KEY:
        return []
    query = _build_query(topic)
    from_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    params = {
        "qInTitle": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_results * 2,
        "apiKey": NEWSAPI_KEY,
    }
    try:
        resp = requests.get(NEWSAPI_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            print(f"[newsapi] Error for '{topic}': {data.get('message')}")
            return []
        articles = []
        for item in data.get("articles", []):
            if not item.get("url") or not item.get("title"):
                continue
            if item.get("title") == "[Removed]":
                continue
            articles.append({
                "title": item["title"],
                "url": item["url"],
                "source": item.get("source", {}).get("name", "NewsAPI"),
                "published_at": item.get("publishedAt", ""),
                "description": item.get("description", "") or "",
            })
        return articles[:max_results]
    except requests.RequestException as e:
        print(f"[newsapi] Request failed for '{topic}': {e}")
        return []
