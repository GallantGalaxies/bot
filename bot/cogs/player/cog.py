import discord
from discord import app_commands
from discord.ext import commands


class PlayerMenuCog(commands.GroupCog, name="player", description="Player commands"):
    """Cog to handle `/player` command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="show", description="Show player")
    async def show(self, interaction: discord.Interaction) -> None:
        """Return interaction response for Player UI."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="join", description="Join voice channel")
    async def join(self, interaction: discord.Interaction) -> None:
        """Join the Voice channel of user."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="play", description="Play selected preset")
    async def play(self, interaction: discord.Interaction) -> None:
        """Play selected preset in the active VC."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="pause", description="Pause current preset")
    async def pause(self, interaction: discord.Interaction) -> None:
        """Pause the current preset that is being player."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="next", description="Play next preset")
    async def next(self, interaction: discord.Interaction) -> None:
        """Play the next preset in the library."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="previous", description="Play previous preset")
    async def previous(self, interaction: discord.Interaction) -> None:
        """Play the previous preset in the library."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="stop", description="Stop current preset")
    async def stop(self, interaction: discord.Interaction) -> None:
        """Stop the current preset that is being played."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(PlayerMenuCog(bot))
