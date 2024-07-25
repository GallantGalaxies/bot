import discord


class BaseEmbed(discord.Embed):
    """Base class for all embeds."""

    def __init__(self, title: str, description: str) -> None:
        super().__init__(title=title, description=description)
        self.set_footer(
            text="Made by the Galant Galaxies",
        )

    def add_image(self, file: discord.File) -> None:
        """Set image."""
        url = f"attachment://{file.filename}"
        self.set_image(url=url)

    def add_field_at(self, index: int, name: str, value: str, inline: str) -> None:
        """Add field at index."""
        is_inline = inline == "YES"
        self.insert_field_at(index=index, name=name, value=value, inline=is_inline)

    def add_thumbnail(self, url: str) -> None:
        """Set thumbnail."""
        self.set_thumbnail(url=url)

    def add_author(self, name: str, icon_url: str) -> None:
        """Set author."""
        self.set_author(name=name, icon_url=icon_url)
