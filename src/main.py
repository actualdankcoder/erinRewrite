import logging
from difflib import get_close_matches
from os import getenv
from pathlib import Path
from typing import List

import arrow
import discord
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

from utils.bindings import AsyncErinDatabase
from utils.create_logger import create_logger

# Configure logger
logger = create_logger(name=__file__, level=logging.DEBUG)
logger.info("Starting Erin...")

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
logger.debug(f"Path to .env file is {env_path}")
assert env_path.exists() and env_path.is_file()
load_dotenv(dotenv_path=env_path)


def load_env_var(var_name: str) -> str:
    logger.debug(f"Loading environment variable {repr(var_name)}")
    var = getenv(var_name)
    if var is None or var == "":
        logger.error(f"Could not find {repr(var_name)} in environment "
                     f"variables!")
        raise ValueError(f"Could not find {repr(var_name)} in environment "
                         f"variables!")
    return var


# Load environment variables
token = load_env_var("BOT_TOKEN")
db_uri = load_env_var("DATABASE_URI")

# Create connection to database
erin_db = AsyncErinDatabase(URI=db_uri)


async def get_prefix(_, message) -> List[str]:
    prefixes = await erin_db.get_prefix(message.guild.id)
    return commands.when_mentioned_or(*prefixes)(erin, message)


class ErinBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=get_prefix, intents=intents,
                         guild_subscriptions=True, case_insensitive=True)
        self.remove_command("help")
        self.startup_time = arrow.utcnow()

    def make_error_embed(self, ctx: commands.Context) -> Embed:
        embed = Embed(color=0xFF0000,
                      timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_author(name=self.user.display_name,
                         icon_url=self.user.avatar_url)
        embed.title = f"Error!"
        return embed


erin = ErinBot()


@erin.event
async def on_command_error(ctx: commands.Context, error):
    embed = erin.make_error_embed(ctx)
    if isinstance(error, commands.errors.CommandOnCooldown):
        embed.description = f"{error}"
    elif isinstance(error, discord.errors.Forbidden):
        embed.description = "Bot has insufficient permissions to perform " \
                            "this action \N{CROSS MARK}"
        if error.text is not None:
            embed.add_field(name="Error reason:", value=error.text)
        if error.code is not None:
            embed.add_field(name="Error code:", value=f"{error.code} "
                                                      f"Forbidden")
        if error.status is not None:
            embed.add_field(name="Error status:", value=str(error.status))
    elif isinstance(error, commands.errors.MissingPermissions):
        embed.description = "Missing permissions \N{CROSS MARK}\n"
        for perms in error.missing_perms:
            missing_perm = str(perms).replace("_", " ").capitalize()
            embed.description += f"\n**{missing_perm}**"
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        embed.description = f"You didn't pass in the required argument(s)\n\n" \
                            f"`{ctx.prefix}{ctx.command.name} " \
                            f"{ctx.command.signature}`\n\n" \
                            f"<> Denotes required argument. " \
                            f"[] Denotes optional argument"
    elif isinstance(error, commands.errors.CommandNotFound):
        prefixes = await erin_db.get_prefix(ctx.message.guild.id)
        command = ctx.message.content
        all_commands = []
        for cmd, obj in erin.all_commands.items():
            if not ctx.channel.is_nsfw() and obj.cog_name.lower() == "nsfw":
                continue
            all_commands.append(cmd)
        for prefix in prefixes:
            try:
                if command.index(prefix) == 0:
                    command = command[len(prefix):]
                    break
            except ValueError:
                pass
        closest = get_close_matches(command, all_commands, n=1)
        if len(closest) == 0:
            closest = ""
        else:
            closest = f"Did you mean `{closest[0]}`?"
        embed.description = f"\"{command}\" isn't a command! {closest}"
    elif isinstance(error, commands.errors.MemberNotFound):
        embed.description = "Could not find the specified member!"
    elif isinstance(error, commands.errors.BadArgument):
        embed.description = "Invalid argument(s) \N{CROSS MARK}\n"
        invalid = ""
        for bad in error.args:
            invalid += f"{bad}\n"
        embed.description += f"\n**{invalid}**\n" \
                             f"Correct command usage: " \
                             f"`{ctx.prefix+ctx.command.name} " \
                             f"{ctx.command.signature}`"
    elif isinstance(error, commands.errors.NoPrivateMessage):
        embed.description = f"`{ctx.prefix}{ctx.command.name}` " \
                            f"does not work in private messages."
    elif isinstance(error, commands.errors.CheckFailure):
        embed.description = "One of the checks failed to validate."
    elif isinstance(error, commands.errors.DisabledCommand):
        embed.description = "This command has been disabled."
    elif isinstance(error, commands.errors.TooManyArguments):
        embed.description = "More than required arguments were passed into " \
                            "this command."
    elif isinstance(error, commands.errors.NotOwner):
        embed.description = "Only the owner can use this command."
    elif isinstance(error, commands.errors.MessageNotFound):
        embed.description = "Couldn't find the requested message."
    elif isinstance(error, commands.errors.UserNotFound):
        embed.description = "Couldn't find the requested user."
    elif isinstance(error, (commands.errors.MissingRole,
                            commands.errors.MissingAnyRole)):
        embed.description = "You do not have the requested role for this command."
    elif isinstance(error, commands.errors.BotMissingPermissions):
        embed.description = "I do not have the permissions to execute the " \
                            "action."
        missing_perms = ""
        for perms in error.missing_perms:
            missing = str(perms).replace("_", " ").capitalize()
            missing_perms += f"{missing}\n"
        embed.add_field(name="Missing perms:", value=missing_perms)
    elif isinstance(error, commands.errors.NSFWChannelRequired):
        embed.description = "Command can only be executed in NSFW channels."
    elif isinstance(error, commands.errors.CommandInvokeError):
        embed.description = "There was an error running this command! " \
                            ":slight_frown:"
        logger.error("There was an error running a command!\n"
                     f"Context: {repr(ctx)}\n"
                     f"Error: {repr(error)}")
    else:
        embed.description = "An unknown error has occurred! :slight_frown:"
        logger.error("An unknown error has occurred!\n"
                     f"Context: {repr(ctx)}\n"
                     f"Error: {repr(error)}")
    await ctx.message.reply(embed=embed)


# Load extensions
logger.info("Loading extensions...")
cog_path = Path(__file__).parent / "cogs"
logger.debug(f"Path to cogs is {cog_path}")
assert cog_path.exists() and cog_path.is_dir()
cogs_loaded = 0
for file in cog_path.iterdir():
    if file.suffix == ".py" and not file.name.startswith("_"):
        ext_path = f"cogs.{file.stem}"
        logger.debug(f"Loading extension \"{ext_path}\"")
        erin.load_extension(ext_path)
        cogs_loaded += 1

erin.run(token)
