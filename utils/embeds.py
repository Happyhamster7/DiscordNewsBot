from datetime import datetime, timezone
import discord
from config import EMBED_COLORS


def _relative_time(published_at: str) -> str:
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        hours = int(delta.total_seconds() // 3600)
        if hours < 1:
            minutes = int(delta.total_seconds() // 60)
            return f"{minutes}m ago"
        if hours < 24:
            return f"{hours}h ago"
        return f"{delta.days}d ago"
    except Exception:
        return ""


def build_digest_embed(topic: str, articles: list, color_index: int = 0) -> discord.Embed:
    color = EMBED_COLORS[color_index % len(EMBED_COLORS)]
    embed = discord.Embed(
        title=f"Topic: {topic.title()}",
        color=color,
    )
    for article in articles:
        title = article.get("title", "No title")
        url = article.get("url", "")
        source = article.get("source", "Unknown")
        published_at = article.get("published_at", "")
        description = article.get("description") or ""
        if len(description) > 120:
            description = description[:117] + "..."

        time_str = _relative_time(published_at)
        meta = f"-# {source} · {time_str}" if time_str else f"-# {source}"

        # Title links to article but URL is hidden (masked hyperlink)
        name = f"[{title}]({url})" if url else title
        value = f"{description}\n{meta}" if description else meta

        embed.add_field(name=name, value=value, inline=False)

    embed.set_footer(text="Powered by multiple sources")
    return embed


def build_no_news_embed(topic: str, color_index: int = 0) -> discord.Embed:
    color = EMBED_COLORS[color_index % len(EMBED_COLORS)]
    return discord.Embed(
        title=f"Topic: {topic.title()}",
        description="No new articles found for this topic.",
        color=color,
    )


def build_header_embed(topic_count: int, article_count: int) -> discord.Embed:
    now = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
    embed = discord.Embed(
        title="News Digest",
        description=f"{now} · {topic_count} topic{'s' if topic_count != 1 else ''} · {article_count} article{'s' if article_count != 1 else ''}",
        color=0x2B2D31,
    )
    return embed
