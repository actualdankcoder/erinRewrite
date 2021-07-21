import logging
from os import getenv
from pathlib import Path

from discord import Embed
from discord.ext import commands
from discord.ext.commands import BucketType
from dotenv import load_dotenv

from src.utils.bindings import AsyncErinDatabase
from src.utils.create_logger import create_logger
from src.utils.exceptions import *

# Configure logger
logger = create_logger(name=__file__, level=logging.DEBUG)

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
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


db_uri = load_env_var("DATABASE_URI")

# Create connection to database
erin_db = AsyncErinDatabase(URI=db_uri)


class Config(commands.Cog):
    """
    Configure parameters about the bot for the server
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def make_embed(self, ctx) -> Embed:
        embed = Embed(color=ctx.message.author.color,
                      timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_author(name=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url)
        return embed

    def make_error_embed(self, ctx) -> Embed:
        embed = Embed(color=0xFF0000,
                      timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_author(name=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url)
        embed.title = f"Error!"
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"\"{self.__class__.__name__}\" cog has been loaded")

    @commands.group(name="prefixes", aliases=["getprefix", "get_prefix",
                                              "getprefixes", "get_prefixes"],
                    case_insensitive=True, description="Gets my prefix(es) "
                                                       "for this server!")
    @commands.cooldown(10, 120, BucketType.guild)
    async def prefixes(self, ctx):
        embed = self.make_embed(ctx)
        embed.set_thumbnail(url=str(ctx.message.guild.icon_url))
        embed.title = f"My prefixes for {ctx.message.guild}"
        prefixes = await erin_db.get_prefix(ctx.message.guild.id)
        all_prefixes = "".join([f"`{prefix}`, " for prefix in prefixes])
        # Remove the ", " from the very end
        all_prefixes = all_prefixes[:-2]
        embed.description = all_prefixes
        await ctx.message.reply(embed=embed)

    @commands.group(name="prefix", aliases=["setprefix", "set_prefix"],
                    case_insensitive=True, description="Sets my prefix for "
                                                       "this server!")
    @commands.cooldown(10, 120, BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = self.make_error_embed(ctx)
            embed.description = "Please mention a sub-command such as " \
                                "`add` or `remove`!"
            await ctx.message.reply(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, *, prefix: str = None):
        embed = self.make_error_embed(ctx)
        if not prefix:
            embed.description = "Please mention a valid prefix to be added!"
            await ctx.message.reply(embed=embed)
            return
        try:
            await erin_db.add_prefix(ctx.message.guild.id, prefix)
        except PrefixError as exc:
            embed.description = str(exc)
        else:
            embed = self.make_embed(ctx)
            embed.set_thumbnail(url=str(ctx.message.guild.icon_url))
            embed.title = "Successfully added prefix!"
            embed.description = f"Successfully added the prefix " \
                                f"\"{prefix}\" to my list of prefixes for " \
                                f"this server!"
        await ctx.message.reply(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, *, prefix: str = None):
        embed = self.make_error_embed(ctx)
        if not prefix:
            embed.description = "Please mention a valid prefix to be remove!"
            await ctx.message.reply(embed=embed)
            return
        try:
            await erin_db.remove_prefix(ctx.message.guild.id, prefix)
        except PrefixError as exc:
            embed.description = str(exc)
        else:
            embed = self.make_embed(ctx)
            embed.set_thumbnail(url=str(ctx.message.guild.icon_url))
            embed.title = "Successfully removed prefix!"
            embed.description = f"Successfully removed the prefix " \
                                f"\"{prefix}\" from my list of prefixes for " \
                                f"this server!"
        await ctx.message.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))
