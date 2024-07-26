from typing import TYPE_CHECKING

import discord
from discord.utils import MISSING

from bot.items import BaseButton, BaseDropdown

if TYPE_CHECKING:
    from discord import Embed
    from discord.ui import View

    from bot.embeds import BaseEmbed


class BaseView(discord.ui.View):
    """Base class for all views.

    Args:
    ----
        interaction (discord.Interaction): The interaction of the view.
        user (int): The user of the view.
        timeout (int, optional): The timeout of the view. Defaults to 180.

    """

    def __init__(
        self,
        interaction: discord.Interaction,
        user: int,
        timeout: int = 180,
    ) -> None:
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.user = user

    async def interaction_check(
        self,
        interaction: discord.Interaction[discord.Client],
    ) -> bool:
        """Check if the interaction is made by the initiated user only."""
        is_user_correct = await super().interaction_check(interaction)
        if not is_user_correct:
            await self.send(
                content="You are not allowed to use this view.",
                ephemeral=True,
            )
            return False
        return True

    async def send(
        self,
        *,
        content: str | None = None,
        embed: "Embed" = MISSING,
        attachments: list[discord.File] = MISSING,
        view: "View" = MISSING,
        ephemeral: bool = False,
        delete_after: int = MISSING,
        edit: bool = False,
    ) -> None:
        """Send view to interaction.

        Args:
        ----
            content (str, optional): The content of the message. Defaults to None.
            embed (Embed, optional): The embed of the message. Defaults to MISSING.
            attachments (list[discord.File], optional): The attachments of the message.
                                                        Defaults to MISSING.
            view (View, optional): The view of the message. Defaults to MISSING.
            ephemeral (bool, optional): The ephemeral of the message. Defaults to False.
            delete_after (int, optional): The delete_after of the message. Defaults to
                                          MISSING.
            edit (bool, optional): The edit of the message. Defaults to False.

        """
        if edit:
            await self.interaction.response.send_message(
                content=content,
                embed=embed,
                view=view,
                ephemeral=ephemeral,
                delete_after=delete_after,
                files=attachments,
            )
        else:
            await self.interaction.response.edit_message(
                content=content,
                embed=embed,
                view=view,
                delete_after=delete_after,
                attachments=attachments,
            )

    async def on_timeout(self) -> None:
        """Remove view on timeout."""
        self.clear_items()
        await self.interaction.response.edit_message(
            view=self,
        )

    async def start(
        self,
        embed_class: "BaseEmbed",
        attachments: list[discord.File],
        view_class: "BaseView",
    ) -> None:
        """Start the view and sends the inital embed."""
        for attachment in attachments:
            embed_class.add_image(attachment)

        await self.send(
            embed=embed_class,
            attachments=attachments,
            view=view_class,
        )

    async def _add_buttons(self, buttons: list[BaseButton]) -> None:
        """Add buttons to the view.

        Args:
        ----
            buttons (list[BaseButton]): The buttons to add to the view.

        """
        for button in buttons:
            self.add_item(button)

    async def _add_dropdowns(self, dropdowns: list[BaseDropdown]) -> None:
        """Add dropdowns to the view.

        Args:
        ----
            dropdowns (list[BaseDropdown]): The dropdowns to add to the view.

        """
        for dropdown in dropdowns:
            self.add_item(dropdown)
