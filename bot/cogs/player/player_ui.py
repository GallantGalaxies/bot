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
            return None
        view: PlayerShowView = self.view
        view.interaction = interaction
        if view.voice_client is None:
            print(f"[{self.custom_id}] Voice client is None")
            return await interaction.response.defer()
        if view.voice_client.is_playing():
            view.voice_client.pause()
        elif view.voice_client.is_paused():
            view.voice_client.resume()
        else:
            # this will run when the user has completed the song
            # or no song has been played
            view.voice_client.play(
                discord.FFmpegPCMAudio(env.PROJECT_ROOT.joinpath("sounds/brown_noise.ogg").as_posix()),
                after=view.preset_play_completion_callback,
            )

        # update embed after changing the state of the player
        view.embed = PlayerEmbed(view.voice_client)
        await view.send(edit=True)
        return None


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
            }

        for name, value in EMBED_FIELDS.items():
            self.add_field(name=name, value=value, inline=False)


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
        buttons = [PlayPauseButton()]
        self._add_buttons(buttons)

    def preset_play_completion_callback(self, error: Exception | None) -> None:
        """Handle completion of preset play."""
        if error:
            print(f"An error occurred: {error}")
        # TODO: Loop the preset
        if self.voice_client:
            self.voice_client.play(
                discord.FFmpegPCMAudio(env.PROJECT_ROOT.joinpath("sounds/brown_noise.ogg").as_posix()),
                after=self.preset_play_completion_callback,
            )
        print("Preset play completed!!")
