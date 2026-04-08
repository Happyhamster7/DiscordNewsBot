from config import ENABLE_NEWSAPI, ENABLE_RSS, ENABLE_GUARDIAN, ENABLE_GNEWS, ENABLE_REDDIT

ENABLED_SOURCES = []

if ENABLE_NEWSAPI:
    from services.sources import newsapi
    ENABLED_SOURCES.append(newsapi)

if ENABLE_RSS:
    from services.sources import rss
    ENABLED_SOURCES.append(rss)

if ENABLE_GUARDIAN:
    from services.sources import guardian
    ENABLED_SOURCES.append(guardian)

if ENABLE_GNEWS:
    from services.sources import gnews
    ENABLED_SOURCES.append(gnews)

if ENABLE_REDDIT:
    from services.sources import reddit
    ENABLED_SOURCES.append(reddit)
