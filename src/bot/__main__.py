import discord
from discord import app_commands
from dotenv import load_dotenv

if True:
    load_dotenv()

from bot.env import env

print(f"Logging level {env.LOGGING_LEVEL}")

GUILD = discord.Object(id=env.GUILD_ID)


class InteractionsClient(discord.Client):
    """Main class for handling Interactions."""

    def __init__(self, *, intents: discord.Intents) -> None:
        """Init new object."""
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self) -> None:
        """Copy the global commands over to your guild."""
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)


intents = discord.Intents.default()
client = InteractionsClient(intents=intents)


@client.event
async def on_ready() -> None:
    """Run when client has logged in."""
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.tree.command()
async def hello(interaction: discord.Interaction) -> None:
    """Says hello!."""
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.


# This context menu command only works on members
@client.tree.context_menu(name="Show Join Date")
async def show_join_date(interaction: discord.Interaction, member: discord.Member) -> None:
    """Show join data on a member context menu."""
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f"{member} joined at {discord.utils.format_dt(member.joined_at)}")


# This context menu command only works on messages
@client.tree.context_menu(name="Get Message Length")
async def send_message_length(interaction: discord.Interaction, message: discord.Message) -> None:
    """Send length of message as interaction response."""
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(f"Message Length is {len(message.content)}", ephemeral=True)


client.run(env.DISCORD_BOT_TOKEN)
