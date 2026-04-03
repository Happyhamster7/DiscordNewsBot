from config import MAX_SEEN_ARTICLES_PER_GUILD


def filter_new_articles(articles: list, seen_urls: list) -> list:
    seen_set = set(seen_urls)
    return [a for a in articles if a.get("url") not in seen_set]


def mark_seen(articles: list, seen_urls: list, max_seen: int = MAX_SEEN_ARTICLES_PER_GUILD) -> list:
    updated = list(seen_urls)
    for a in articles:
        url = a.get("url")
        if url and url not in updated:
            updated.append(url)
    return updated[-max_seen:]
