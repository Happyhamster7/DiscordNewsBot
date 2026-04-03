import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import load_store, save_store


class ChannelConfigCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setchannel", description="Set the channel where news digests will be posted (admin only)")
    @app_commands.default_permissions(manage_guild=True)
    async def setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if interaction.guild_id is None:
            await interaction.response.send_message("This bot only works in servers.", ephemeral=True)
            return

        store = load_store()
        guild_id = str(interaction.guild_id)
        store["guilds"].setdefault(guild_id, {})
        store["guilds"][guild_id]["digest_channel_id"] = str(channel.id)
        save_store(store)

        await interaction.response.send_message(
            f"News digest channel set to {channel.mention}.", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelConfigCog(bot))
