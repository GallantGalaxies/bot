import discord

from bot.embeds import BaseEmbed
from bot.env import env
from bot.items import BaseButton
from bot.views import BaseView


class PlayPauseButton(BaseButton):
    """Button to Play or Pause the sound being played."""

    def __init__(self) -> None:
        super().__init__(label="⏯", custom_id="player-play-pause")

    async def callback(self, interaction: discord.Interaction) -> None:
        """Play or Pause the sound being played."""
        if self.view is None:
            return
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            await interaction.response.defer()
            await interaction.followup.send("Please join a Voice Channel 🙂", ephemeral=True)
            return
        if view.voice_client.is_playing():
            view.voice_client.pause()
        elif view.voice_client.is_paused():
            view.voice_client.resume()
        else:
            # this will run when the user has completed the song
            # or no song has been played
            view.voice_client.play(
                discord.PCMVolumeTransformer(
                    original=discord.FFmpegPCMAudio(env.PROJECT_ROOT.joinpath("sounds/brown_noise.ogg").as_posix()),
                    volume=view.voice_client.source.volume
                    if isinstance(view.voice_client.source, discord.PCMVolumeTransformer)
                    else 0.5,
                ),
                after=view.preset_play_completion_callback,
            )

        # update embed after changing the state of the player
        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)
        return


class NextButton(BaseButton):
    """Button to Play or Pause the sound being played."""

    def __init__(self) -> None:
        super().__init__(label="⏭", custom_id="player-next")

    async def callback(self, interaction: discord.Interaction) -> None:
        """Play or Pause the sound being played."""
        if self.view is None:
            return
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            await interaction.response.defer()
            await interaction.followup.send("Please join a Voice Channel 🙂", ephemeral=True)
            return
        # TODO: Add next song

        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)
        return


class PreviousButton(BaseButton):
    """Button to Play or Pause the sound being played."""

    def __init__(self) -> None:
        super().__init__(label="⏮", custom_id="player-previous")

    async def callback(self, interaction: discord.Interaction) -> None:
        """Play or Pause the sound being played."""
        if self.view is None:
            return
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            await interaction.response.defer()
            await interaction.followup.send("Please join a Voice Channel 🙂", ephemeral=True)
            return
        # TODO: Add previous song

        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)


class MuteUnmuteButton(BaseButton):
    """Button to Play or Pause the sound being played."""

    def __init__(self) -> None:
        super().__init__(label="🔇", custom_id="player-mute", row=2)

    async def callback(self, interaction: discord.Interaction) -> None:
        """Play or Pause the sound being played."""
        if self.view is None:
            return
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            await interaction.response.defer()
            await interaction.followup.send("Please join a Voice Channel 🙂", ephemeral=True)
            return
        vol = view.voice_client.source.volume
        if vol == 0.0:
            view.voice_client.source.volume = 1.0
        else:
            view.voice_client.source.volume = 0.0

        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)
        return


class VolumeUpButton(BaseButton):
    """Button to Play or Pause the sound being played."""

    def __init__(self) -> None:
        super().__init__(label="🔊", custom_id="player-volume-up", row=2)

    async def callback(self, interaction: discord.Interaction) -> None:
        """Play or Pause the sound being played."""
        if self.view is None:
            return
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            await interaction.response.defer()
            await interaction.followup.send("Please join a Voice Channel 🙂", ephemeral=True)
            return
        vol = view.voice_client.source.volume
        view.voice_client.source.volume = min(1.0, vol + 0.1)

        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)
        return


class VolumeDownButton(BaseButton):
    """Button to Play or Pause the sound being played."""

    def __init__(self) -> None:
        super().__init__(label="🔉", custom_id="player-volume-down", row=2)

    async def callback(self, interaction: discord.Interaction) -> None:
        """Play or Pause the sound being played."""
        if self.view is None:
            return
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            await interaction.response.defer()
            await interaction.followup.send("Please join a Voice Channel 🙂", ephemeral=True)
            return
        vol = view.voice_client.source.volume
        view.voice_client.source.volume = max(0.0, vol - 0.1)

        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)
        return


class PlayerEmbed(BaseEmbed):
    """Embed to show the player UI."""

    def __init__(self, voice_client: discord.VoiceClient) -> None:
        super().__init__(title="Player UI")
        if voice_client is None:
            EMBED_FIELDS = {"Channel": "Not Connected", "Status": "Not Playing"}  # noqa: N806
        else:
            EMBED_FIELDS = {  # noqa: N806
                "Channel": voice_client.channel.mention if voice_client.channel is not None else "Not Playing",
                "Status": "Not Playing"
                if voice_client.source is None
                else ("Playing" if voice_client.is_playing() else "Paused"),
                "Volume": f"{voice_client.source.volume * 100:.0f}%"
                if isinstance(voice_client.source, discord.PCMVolumeTransformer)
                else "Not Playing",
            }

        for name, value in EMBED_FIELDS.items():
            self.add_field(name=name, value=value, inline=name in ("Status", "Volume"))


class PlayerShowView(BaseView):
    """View to show the player UI."""

    def __init__(self, interaction: discord.Interaction, voice_client: discord.VoiceClient) -> None:
        super().__init__(
            interaction,
            user=interaction.user.id,
            content="Player UI",
            timeout=None,
            embed=PlayerEmbed(voice_client),
        )

        self.voice_client = voice_client
        buttons = [
            NextButton(),
            PlayPauseButton(),
            PreviousButton(),
            MuteUnmuteButton(),
            VolumeDownButton(),
            VolumeUpButton(),
        ]
        self._add_buttons(buttons)

    def preset_play_completion_callback(self, error: Exception | None) -> None:
        """Handle completion of preset play."""
        if error:
            print(f"An error occurred: {error}")
        # TODO: Loop the preset
        if self.voice_client:
            self.voice_client.play(
                discord.PCMVolumeTransformer(
                    original=discord.FFmpegPCMAudio(env.PROJECT_ROOT.joinpath("sounds/brown_noise.ogg").as_posix()),
                    volume=0.5,
                ),
                after=self.preset_play_completion_callback,
            )
        print("Preset play completed!!")
