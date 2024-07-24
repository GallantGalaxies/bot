import discord
from discord import app_commands
from discord.ext import commands


class AboutMenuCog(commands.Cog):
    """Cog to handle `/about` command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="about", description="Information about the bot.")
    async def send_ui(self, interaction: discord.Interaction) -> None:
        """Return interaction response for About UI."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!, Changed", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(AboutMenuCog(bot))
