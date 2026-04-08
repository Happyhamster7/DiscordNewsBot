import datetime
import feedparser
import requests

RSS_URL = "https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
HEADERS = {"User-Agent": "discord-news-bot/1.0"}


def fetch(topic: str, max_results: int = 2) -> list:
    try:
        url = RSS_URL.format(topic=topic.replace(" ", "+"))
        feed = feedparser.parse(url, request_headers=HEADERS)
        articles = []
        for entry in feed.entries[:max_results]:
            published = ""
            if entry.get("published_parsed"):
                try:
                    published = datetime.datetime(*entry.published_parsed[:6]).isoformat() + "Z"
                except Exception:
                    pass

            source = "Google News RSS"
            if hasattr(entry, "source") and isinstance(entry.source, dict):
                source = entry.source.get("title", source)

            url_str = entry.get("link", "")
            title = entry.get("title", "No title")
            description = entry.get("summary", "") or ""

            if not url_str or not title:
                continue

            articles.append({
                "title": title,
                "url": url_str,
                "source": source,
                "published_at": published,
                "description": description,
            })
        return articles
    except Exception as e:
        print(f"[rss] Failed for '{topic}': {e}")
        return []
