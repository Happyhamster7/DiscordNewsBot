import re
import requests
from config import GUARDIAN_API_KEY

BASE_URL = "https://content.guardianapis.com/search"


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def fetch(topic: str, max_results: int = 2) -> list:
    if not GUARDIAN_API_KEY:
        return []
    try:
        params = {
            "q": topic,
            "api-key": GUARDIAN_API_KEY,
            "page-size": max_results,
            "show-fields": "trailText",
            "order-by": "newest",
        }
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("response", {}).get("results", [])
        articles = []
        for r in results[:max_results]:
            description = _strip_html(r.get("fields", {}).get("trailText", "") or "")
            articles.append({
                "title": r.get("webTitle", "No title"),
                "url": r.get("webUrl", ""),
                "source": "The Guardian",
                "published_at": r.get("webPublicationDate", ""),
                "description": description,
            })
        return articles
    except Exception as e:
        print(f"[guardian] Failed for '{topic}': {e}")
        return []
