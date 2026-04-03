from config import MAX_TOPICS_PER_DIGEST


def get_all_topics(guild_id: str, store: dict, extra_topics: list | None = None) -> list:
    """Return a sorted, deduplicated list of topics for a guild.

    extra_topics is the future hook for conversation-derived topics —
    pass them here and the rest of the pipeline needs no changes.
    """
    topics = set()
    for user_data in store.get("users", {}).values():
        if str(user_data.get("guild_id")) == str(guild_id):
            for interest in user_data.get("interests", []):
                if interest and interest.strip():
                    topics.add(interest.strip().lower())
    if extra_topics:
        for t in extra_topics:
            if t and t.strip():
                topics.add(t.strip().lower())
    return sorted(topics)[:MAX_TOPICS_PER_DIGEST]
