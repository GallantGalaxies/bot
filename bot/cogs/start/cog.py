import discord
from discord import app_commands
from discord.ext import commands


class StartMenuCog(commands.Cog):
    """Cog to handle `/start` command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="start", description="Start your journey")
    async def send_ui(self, interaction: discord.Interaction) -> None:
        """Return interaction response Start UI."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(StartMenuCog(bot))
