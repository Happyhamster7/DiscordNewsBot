import discord
from discord import app_commands
from discord.ext import commands, tasks
from config import NEWSAPI_KEY, SCHEDULE_HOURS
from utils.storage import load_store, save_store
from utils.embeds import build_digest_embed, build_no_news_embed, build_header_embed
from services.topic_aggregator import get_all_topics
from services.news_fetcher import fetch_articles
from services.deduplicator import filter_new_articles, mark_seen


class DigestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_unload(self):
        self.scheduled_digest.cancel()

    @tasks.loop(hours=SCHEDULE_HOURS)
    async def scheduled_digest(self):
        store = load_store()
        for guild_id, guild_data in store.get("guilds", {}).items():
            channel_id = guild_data.get("digest_channel_id")
            if not channel_id:
                continue
            channel = self.bot.get_channel(int(channel_id))
            if channel is None:
                continue
            await self.run_digest(guild_id, channel)

    @scheduled_digest.before_loop
    async def before_digest(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="news", description="Manually trigger the news digest right now")
    async def news(self, interaction: discord.Interaction):
        if interaction.guild_id is None:
            await interaction.response.send_message("This bot only works in servers.", ephemeral=True)
            return

        guild_id = str(interaction.guild_id)
        store = load_store()
        channel_id = store.get("guilds", {}).get(guild_id, {}).get("digest_channel_id")
        if not channel_id:
            await interaction.response.send_message(
                "No digest channel set. An admin must run `/setchannel` first.", ephemeral=True
            )
            return

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            await interaction.response.send_message(
                "Could not find the configured digest channel.", ephemeral=True
            )
            return

        await interaction.response.send_message("Fetching news digest...", ephemeral=True)
        await self.run_digest(guild_id, channel)

    async def run_digest(self, guild_id: str, channel: discord.TextChannel):
        store = load_store()
        topics = get_all_topics(guild_id, store)

        if not topics:
            return

        seen_urls = store.get("seen_articles", {}).get(guild_id, [])
        embeds = []
        all_new_articles = []

        for i, topic in enumerate(topics):
            raw_articles = fetch_articles(topic, NEWSAPI_KEY)
            new_articles = filter_new_articles(raw_articles, seen_urls)[:3]

            if new_articles:
                embeds.append(build_digest_embed(topic, new_articles, color_index=i))
                all_new_articles.extend(new_articles)
            else:
                embeds.append(build_no_news_embed(topic, color_index=i))

        if not embeds:
            return

        header = build_header_embed(
            topic_count=len(topics),
            article_count=len(all_new_articles),
        )

        try:
            await channel.send(embed=header)
            for embed in embeds:
                await channel.send(embed=embed)
        except discord.Forbidden:
            print(f"[digest] Missing permissions to post in channel {channel.id}")
            return

        seen_urls = mark_seen(all_new_articles, seen_urls)
        store.setdefault("seen_articles", {})[guild_id] = seen_urls
        save_store(store)

    @app_commands.command(name="status", description="Show current bot configuration for this server")
    async def status(self, interaction: discord.Interaction):
        if interaction.guild_id is None:
            await interaction.response.send_message("This bot only works in servers.", ephemeral=True)
            return

        guild_id = str(interaction.guild_id)
        store = load_store()
        guild_data = store.get("guilds", {}).get(guild_id, {})
        channel_id = guild_data.get("digest_channel_id")
        channel_mention = f"<#{channel_id}>" if channel_id else "Not set"

        user_count = sum(
            1 for u in store.get("users", {}).values()
            if str(u.get("guild_id")) == guild_id
        )
        topics = get_all_topics(guild_id, store)

        next_run = "Running" if self.scheduled_digest.is_running() else "Not started"

        embed = discord.Embed(title="Bot Status", color=0x5865F2)
        embed.add_field(name="Digest Channel", value=channel_mention, inline=False)
        embed.add_field(name="Users with Interests", value=str(user_count), inline=True)
        embed.add_field(name="Unique Topics", value=str(len(topics)), inline=True)
        embed.add_field(name="Schedule", value=f"Every {SCHEDULE_HOURS}h ({next_run})", inline=True)
        if topics:
            embed.add_field(name="Current Topics", value=", ".join(t.title() for t in topics), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(DigestCog(bot))
