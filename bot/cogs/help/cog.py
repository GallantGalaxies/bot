import discord
from discord import app_commands
from discord.ext import commands


class HelpMenuCog(commands.Cog):
    """Cog to handle `/help` command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Show help menu")
    async def send_ui(self, interaction: discord.Interaction) -> None:
        """Return interaction response for Help UI."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!, Changed", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(HelpMenuCog(bot))
