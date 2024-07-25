from pathlib import Path

import discord
from discord import app_commands
from discord._types import ClientT
from discord.ext import commands


class PlayerMenuCog(commands.GroupCog, name="player", description="Player commands"):
    """Cog to handle `/player` command."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.voice_client: discord.VoiceClient | None = None

    def interaction_check(self, interaction: discord.Interaction[ClientT], /) -> bool:
        """Check if the interaction is valid."""
        self.voice_client = interaction.guild.voice_client
        return True

    @app_commands.command(name="show", description="Show player")
    async def show(self, interaction: discord.Interaction) -> None:
        """Return interaction response for Player UI."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        await response.send_message("Not Yet Implemented!!", ephemeral=True)

    @app_commands.command(name="join", description="Join voice channel")
    async def join(self, interaction: discord.Interaction) -> None:
        """Join the Voice channel of user."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        if interaction.user.voice is None:
            await response.send_message("Please join a Voice Channel 🙂", ephemeral=True)
            return

        voice_channel: discord.VoiceChannel = interaction.user.voice.channel
        if self.voice_client:
            await response.send_message(f"Connected to {voice_channel.mention}", ephemeral=True)
            return

        self.voice_client: discord.VoiceClient = await voice_channel.connect(self_deaf=True)
        await response.send_message(f"Connected to {voice_channel.mention}", ephemeral=True)

    @app_commands.command(name="play", description="Play selected preset")
    async def play(self, interaction: discord.Interaction) -> None:
        """Play selected preset in the active VC."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]

        if self.voice_client is None:
            await response.send_message("Please join a Voice Channel 🙂", ephemeral=True)
            return

        if self.voice_client.is_playing():
            await response.send_message(
                f"A preset is already being player in {self.voice_client.channel.mention}",
                ephemeral=True,
            )
            return
        if self.voice_client.is_paused():
            self.voice_client.resume()
            await response.send_message(f"Resuming playing in {self.voice_client.channel.mention}", ephemeral=True)
            return

        self.voice_client.play(
            discord.FFmpegPCMAudio(Path(__file__).joinpath("song.flac").as_posix()),
        )
        await response.send_message(f"Playing preset in {self.voice_client.channel.mention}", ephemeral=True)

    @app_commands.command(name="pause", description="Pause current preset")
    async def pause(self, interaction: discord.Interaction) -> None:
        """Pause the current preset that is being player."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        if self.voice_client is None:
            await response.send_message("Please join a Voice Channel First🙂", ephemeral=True)
            return

        if self.voice_client.is_paused():
            await response.send_message("Already Paused!!", ephemeral=True)
            return

        if self.voice_client.is_playing():
            self.voice_client.pause()
            await response.send_message("Paused!!", ephemeral=True)

    @app_commands.command(name="stop", description="Stop current preset")
    async def stop(self, interaction: discord.Interaction) -> None:
        """Stop the current preset that is being played."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        if self.voice_client is None:
            await response.send_message("Please join a Voice Channel First🙂", ephemeral=True)
            return

        if self.voice_client.is_playing() or self.voice_client.is_paused():
            self.voice_client.stop()
            await response.send_message("Stopped!!", ephemeral=True)
            return

        await response.defer()

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

    @app_commands.command(name="volume", description="Set volume of player")
    async def volume(self, interaction: discord.Interaction, volume: float) -> None:
        """Set the volume of the player."""
        response: discord.InteractionResponse = interaction.response  # type: ignore[attr-defined]
        self.voice_client.source.volume = volume if 0 <= volume <= 1 else 0.5
        await response.send_message(f"Volume set to {volume}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(PlayerMenuCog(bot))
