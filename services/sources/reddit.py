import datetime
import requests

BASE_URL = "https://www.reddit.com/search.json"
HEADERS = {"User-Agent": "discord-news-bot/1.0"}


def fetch(topic: str, max_results: int = 2) -> list:
    try:
        params = {"q": topic, "sort": "new", "limit": max_results, "type": "link"}
        resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        children = resp.json().get("data", {}).get("children", [])
        articles = []
        for child in children[:max_results]:
            p = child.get("data", {})
            url = p.get("url", "")
            title = p.get("title", "No title")
            if not url or not title:
                continue
            ts = p.get("created_utc", 0)
            try:
                published = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                published = ""
            description = p.get("selftext", "")[:300] if p.get("selftext") else ""
            articles.append({
                "title": title,
                "url": url,
                "source": f"Reddit r/{p.get('subreddit', 'all')}",
                "published_at": published,
                "description": description,
            })
        return articles
    except Exception as e:
        print(f"[reddit] Failed for '{topic}': {e}")
        return []
