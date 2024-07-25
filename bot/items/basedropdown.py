from typing import Protocol

import discord


class DropdownCallback(Protocol):
    """Base class for all dropdown callbacks."""

    async def __call__(self, interaction: discord.Interaction) -> None:
        """Call the dropdown callback."""
        ...


class BaseDropdown(discord.ui.Select):  # type: ignore  # noqa: PGH003
    """Base class for all dropdowns.

    Args:
    ----
        custom_id (str): The custom id of the dropdown.
        options (dict[str, str]): The options of the dropdown.
        dropdown_callback (DropdownCallback): The callback of the dropdown.
        placeholder (str, optional): The placeholder of the dropdown. Defaults to None.
        min_values (int, optional): The minimum number of values. Defaults to 1.
        max_values (int, optional): The maximum number of values. Defaults to 1.
        row (int, optional): The row of the dropdown. Defaults to None.
        disabled (bool, optional): The state of the dropdown. Defaults to False.

    """

    def __init__(
        self,
        *,
        custom_id: str,
        options: dict[str, str],
        dropdown_callback: DropdownCallback,
        placeholder: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        row: int | None = None,
        disabled: bool = False,
    ) -> None:
        if not disabled and len(options) == 0:
            options = {"No options available": "NO_OPTIONS"}
            disabled = True

        dropdown_options: list[discord.SelectOption] = [
            discord.SelectOption(label=label, value=value) for label, value in options.items()
        ]

        super().__init__(
            custom_id=custom_id,
            options=dropdown_options,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            row=row,
            disabled=disabled,
        )

        self.dropdown_callback = dropdown_callback

    async def callback(self, interaction: discord.Interaction) -> None:
        """Call the dropdown callback."""
        await self.dropdown_callback(interaction=interaction)
