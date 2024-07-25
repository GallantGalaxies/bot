from typing import Protocol

import discord


class ButtonCallback(Protocol):
    """Base class for all button callbacks."""

    async def __call__(self, interaction: discord.Interaction) -> None:
        """Call the button callback."""
        ...


class BaseButton(discord.ui.Button):  # type: ignore  # noqa: PGH003
    """Base class for all buttons.

    Args:
    ----
        label (str): The label of the button.
        button_callback (ButtonCallback): The callback of the button.
        disabled (bool, optional): The state of the button. Defaults to False.
        custom_id (str): The custom id of the button.
        row (int, optional): The row of the button. Defaults to None.
        button_style (discord.ButtonStyle, optional): The style of the button. Defaults
                                                      to discord.ButtonStyle.green.

    """

    def __init__(
        self,
        *,
        label: str,
        button_callback: ButtonCallback,
        disabled: bool = False,
        custom_id: str,
        row: int | None = None,
        button_style: discord.ButtonStyle = discord.ButtonStyle.green,
    ) -> None:
        super().__init__(
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            row=row,
            style=button_style,
        )
        self.button_callback = button_callback

    async def callback(self, interaction: discord.Interaction) -> None:
        """Call the button callback."""
        await self.button_callback(interaction=interaction)
