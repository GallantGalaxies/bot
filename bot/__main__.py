from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

if True:
    load_dotenv()

from bot.env import env

print(f"Logging level {env.LOGGING_LEVEL}")

GUILD = discord.Object(id=env.GUILD_ID)


class InteractionsBot(commands.Bot):
    """Main class for handling Interactions."""

    def __init__(self, *, intents: discord.Intents) -> None:
        """Init new object."""
        super().__init__("!", intents=intents)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self) -> None:
        """Copy the global commands over to your guild."""
        cog_files = list(filter(lambda x: x.stem != "__init__", (Path(__file__).parent / "cogs").glob("*.py")))
        for file in cog_files:
            print(f"loading {file.name}")
            await self.load_extension(f"bot.cogs.{file.stem}")
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)


intents = discord.Intents.default()
bot = InteractionsBot(intents=intents)


@bot.event
async def on_ready() -> None:
    """Run when client has logged in."""
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(list(bot.cogs))
    print("------")


@bot.tree.command()
async def hello(interaction: discord.Interaction) -> None:
    """Says hello!."""
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.


# This context menu command only works on members
@bot.tree.context_menu(name="Show Join Date")
async def show_join_date(interaction: discord.Interaction, member: discord.Member) -> None:
    """Show join data on a member context menu."""
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f"{member} joined at {discord.utils.format_dt(member.joined_at)}")


# This context menu command only works on messages
@bot.tree.context_menu(name="Get Message Length")
async def send_message_length(interaction: discord.Interaction, message: discord.Message) -> None:
    """Send length of message as interaction response."""
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(f"Message Length is {len(message.content)}", ephemeral=True)


def start() -> None:
    """Entry point for poetry."""
    bot.run(env.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    start()
