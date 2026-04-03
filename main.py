import discord
from discord.ext import commands
from config import DISCORD_TOKEN, DEV_GUILD_ID

# NOTE: When adding conversation reading in v2, enable message_content intent here
# AND in the Discord Developer Portal (Bot > Privileged Gateway Intents).
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")

    # Sync slash commands.
    # DEV_GUILD_ID syncs instantly (for development).
    # Remove it (or leave DEV_GUILD_ID blank) for global sync — takes up to 1 hour.
    if DEV_GUILD_ID:
        guild = discord.Object(id=int(DEV_GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"Slash commands synced to dev guild {DEV_GUILD_ID}")
    else:
        await bot.tree.sync()
        print("Slash commands synced globally")

    # Start the scheduled digest task (guard against on_ready firing multiple times)
    digest_cog = bot.cogs.get("DigestCog")
    if digest_cog and not digest_cog.scheduled_digest.is_running():
        digest_cog.scheduled_digest.start()
        print("Digest task started (daily at 11:00am Australia/Sydney)")


async def main():
    async with bot:
        await bot.load_extension("cogs.channel_config")
        await bot.load_extension("cogs.interests")
        await bot.load_extension("cogs.digest")
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
