import requests
from datetime import datetime, timedelta, timezone
from config import MAX_ARTICLES_PER_TOPIC

NEWSAPI_URL = "https://newsapi.org/v2/everything"


def _build_query(topic: str) -> str:
    """Wrap multi-word topics in quotes for exact phrase matching."""
    topic = topic.strip()
    if " " in topic:
        return f'"{topic}"'
    return topic


def fetch_articles(topic: str, api_key: str, max_results: int = MAX_ARTICLES_PER_TOPIC) -> list:
    """Fetch news articles for a given topic from NewsAPI.

    Uses qInTitle so only articles with the topic in the headline are
    returned — much more relevant than full-body search.

    Returns a normalized list of dicts:
      [{title, url, source, published_at, description}]
    Returns empty list on any error.
    """
    query = _build_query(topic)
    from_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    params = {
        "qInTitle": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_results * 2,  # fetch extra for dedup headroom
        "apiKey": api_key,
    }
    try:
        resp = requests.get(NEWSAPI_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            print(f"[news_fetcher] NewsAPI error for '{topic}': {data.get('message')}")
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
                "source": item.get("source", {}).get("name", "Unknown"),
                "published_at": item.get("publishedAt", ""),
                "description": item.get("description", ""),
            })
        return articles
    except requests.RequestException as e:
        print(f"[news_fetcher] Request failed for '{topic}': {e}")
        return []


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv("NEWSAPI_KEY")
    results = fetch_articles("artificial intelligence", key)
    for a in results:
        print(f"- {a['title']} ({a['source']})")
