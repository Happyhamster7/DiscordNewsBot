import discord
from discord import app_commands, ui
from discord.ext import commands
from utils.storage import load_store, save_store


class InterestsModal(ui.Modal, title="Set Your Top 3 Interests"):
    interest1 = ui.TextInput(label="Interest 1", placeholder="e.g. politics", max_length=50)
    interest2 = ui.TextInput(label="Interest 2", placeholder="e.g. AI research", max_length=50)
    interest3 = ui.TextInput(label="Interest 3", placeholder="e.g. climate", max_length=50)

    def __init__(self, guild_id: int, existing: list):
        super().__init__()
        self.guild_id = guild_id
        if len(existing) > 0:
            self.interest1.default = existing[0]
        if len(existing) > 1:
            self.interest2.default = existing[1]
        if len(existing) > 2:
            self.interest3.default = existing[2]

    async def on_submit(self, interaction: discord.Interaction):
        interests = [
            str(self.interest1).strip(),
            str(self.interest2).strip(),
            str(self.interest3).strip(),
        ]
        interests = [i for i in interests if i]
        if not interests:
            await interaction.response.send_message("Please enter at least one interest.", ephemeral=True)
            return

        store = load_store()
        store["users"][str(interaction.user.id)] = {
            "interests": interests,
            "guild_id": str(self.guild_id),
        }
        save_store(store)

        formatted = ", ".join(f"**{i}**" for i in interests)
        await interaction.response.send_message(
            f"Your interests have been saved: {formatted}", ephemeral=True
        )


class InterestsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setinterests", description="Set your top 3 interests for the news digest")
    async def setinterests(self, interaction: discord.Interaction):
        if interaction.guild_id is None:
            await interaction.response.send_message("This bot only works in servers.", ephemeral=True)
            return
        store = load_store()
        existing = store.get("users", {}).get(str(interaction.user.id), {}).get("interests", [])
        await interaction.response.send_modal(InterestsModal(guild_id=interaction.guild_id, existing=existing))


async def setup(bot: commands.Bot):
    await bot.add_cog(InterestsCog(bot))
