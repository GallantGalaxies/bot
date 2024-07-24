import discord
from discord import app_commands
from discord.ext import commands


class PresetMenuCog(commands.Cog):
    """Cog to handle `/preset` command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="preset", description="Edit a Preset")
    async def send_ui(self, interaction: discord.Interaction) -> None:
        """Return interaction response for Preset UI."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(PresetMenuCog(bot))
