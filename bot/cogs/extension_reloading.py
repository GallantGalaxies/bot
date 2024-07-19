import secrets
from enum import Enum
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

cogs_blacklist = ["__init__"]
cogs_list = " ".join(
    [cog_file.stem for cog_file in filter(lambda x: x.stem not in cogs_blacklist, Path(__file__).parent.glob("*.py"))],
)


CogsEnum = Enum("CogsEnum", cogs_list)

GOOD_STATUS_EMOJI = ["✅", "👍"]
BAD_STATUS_EMOJI = ["❌", "👎"]


class ReloaderCog(commands.Cog):
    """Cog to handle Ping-Pong command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="reload", description="Will reload a cog")
    @app_commands.describe(cog_name="Name of the cog you want to reload.")
    async def reload(self, interaction: discord.Interaction, cog_name: CogsEnum) -> None:
        """Reload cog that matches cog_name."""
        response_embed = discord.Embed(title="Reload Status")
        response_embed.add_field(name="Cog Name", value=cog_name.name, inline=True)
        response_embed.add_field(name="status", value="🔄")
        await interaction.response.send_message(embeds=[response_embed])
        await self.bot.reload_extension(f"bot.cogs.{cog_name.name}")

        response_embed.remove_field(1)
        response_embed.add_field(name="status", value=secrets.choice(GOOD_STATUS_EMOJI))
        await interaction.edit_original_response(embeds=[response_embed])


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(ReloaderCog(bot))
