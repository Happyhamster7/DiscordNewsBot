import requests
from config import GNEWS_API_KEY

BASE_URL = "https://gnews.io/api/v4/search"


def fetch(topic: str, max_results: int = 2) -> list:
    if not GNEWS_API_KEY:
        return []
    try:
        params = {
            "q": topic,
            "token": GNEWS_API_KEY,
            "lang": "en",
            "max": max_results,
        }
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        articles = []
        for a in resp.json().get("articles", [])[:max_results]:
            articles.append({
                "title": a.get("title", "No title"),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", "GNews"),
                "published_at": a.get("publishedAt", ""),
                "description": a.get("description", "") or "",
            })
        return articles
    except Exception as e:
        print(f"[gnews] Failed for '{topic}': {e}")
        return []
