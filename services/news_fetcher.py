from config import MAX_ARTICLES_PER_TOPIC
from services.sources import ENABLED_SOURCES


def fetch_articles(topic: str, max_results: int = MAX_ARTICLES_PER_TOPIC) -> list:
    """Fetch and aggregate articles from all enabled news sources.

    Spreads max_results across sources and deduplicates by URL.
    Returns a normalized list of dicts: [{title, url, source, published_at, description}]
    """
    if not ENABLED_SOURCES:
        return []

    per_source = max(1, max_results // len(ENABLED_SOURCES))
    seen_urls = set()
    results = []

    for source in ENABLED_SOURCES:
        try:
            articles = source.fetch(topic, max_results=per_source)
        except Exception as e:
            print(f"[news_fetcher] Source {source.__name__} failed for '{topic}': {e}")
            articles = []

        for article in articles:
            url = article.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                results.append(article)

    return results[:max_results]
