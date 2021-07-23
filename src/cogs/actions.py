import logging
from os import getenv
from pathlib import Path
from typing import Union

import aiohttp
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import BucketType
from dotenv import load_dotenv

from src.utils.bindings import AsyncErinDatabase
from src.utils.create_logger import create_logger

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


class Action(commands.Cog):
    """
    Action commands such as lick, hug, and kiss
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

    async def api_call(self, url: str,
                       return_text: bool = False) -> Union[dict, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if return_text:
                    return await response.text()
                else:
                    return await response.json()

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="hug", description="Hug someone UwU")
    async def hug(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna hug in the "
                                    f"command ;)")
            return
        hugged_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "aww hugs uwu"
        embed.description = f"{ctx.author.mention} just hugged {hugged_users}"
        response = await self.api_call("https://nekos.life/api/v2/img/hug")
        url = response["url"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="laugh",
                      description="LMFAO <:KEKW:791927881319448606>")
    async def laugh(self, ctx, user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna laugh at in "
                                    f"the command ;)")
            return
        laughed_at = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "AHAHAHAH!!"
        embed.description = f"{ctx.author.mention} just laughed at " \
                            f"{laughed_at}"
        response = await self.api_call("http://api.nekos.fun:8080/api/laugh")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Action(bot))
