import discord
from discord import app_commands
from discord.ext import commands


class PingCog(commands.Cog):
    """Cog to handle Ping-Pong command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="command that tells you ping")
    async def send_ping(self, interaction: discord.Interaction) -> None:
        """Return interaction response with Pong."""
        bot_latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.")


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(PingCog(bot))
