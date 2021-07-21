import logging
from os import getenv
from pathlib import Path

from discord import Embed, HTTPException
from discord.ext import commands
from discord.ext.commands import BucketType
from dotenv import load_dotenv
import aiohttp

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


class Fun(commands.Cog):
    """
    What fun in this category
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def make_embed(self, ctx):
        embed = Embed(color=ctx.message.author.color,
                      timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_author(name=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url)
        return embed

    def make_error_embed(self, ctx):
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

    async def api_call(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="furrify", aliases=["furry", "uwu", "uwuify",
                                               "owo", "owoify"],
                      description="Makes youw text fuwwy uwu")
    async def furrify(self, ctx, *, msg: str = ""):
        embed = self.make_error_embed(ctx)
        if len(msg) == 0:
            embed.description = "NYo text pwovided to uwuify owo"
            await ctx.send(embed=embed)
            return
        elif len(msg) > 200:
            embed.description = f"Thewe's too much text owo\n" \
                                f"(You passed iny {len(msg)} chawactews but " \
                                f"the wimit is 200)"
            await ctx.send(embed=embed)
            return
        try:
            await ctx.message.delete()
        except HTTPException:
            pass
        response = await self.api_call(f"https://nekos.life/api/v2/owoify?"
                                       f"text={msg}")
        try:
            uwu_text = response["owo"]
        except KeyError:
            embed.description = "API ewwow occuwed :cry:"
            await ctx.send(embed=embed)
        else:
            await ctx.send(uwu_text)

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="8ball", aliases=["8_ball", "ball", "eightball",
                                             "eight_ball"],
                      description="Let the magic 8ball decide your fate 😈")
    async def ball(self, ctx, *, question: str = ""):
        embed = self.make_error_embed(ctx)
        if len(question) == 0:
            embed.description = "No question was provided!"
            await ctx.send(embed=embed)
            return
        embed = self.make_embed(ctx)
        response = await self.api_call("https://nekos.life/api/v2/8ball")
        embed.title = "8ball 🎱"
        try:
            embed.description = response["response"]
            embed.set_thumbnail(url=response["url"])
        except KeyError:
            embed = self.make_error_embed(ctx)
            embed.description = "API error occurred! :cry:"
            await ctx.send(embed=embed)
        else:
            await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 3, BucketType.user)
    @commands.command(name="coffee",
                      description="Shows a picture of coffee :smirk:")
    async def coffee(self, ctx):
        response = await self.api_call("https://coffee.alexflipnote.dev/random.json")
        embed = self.make_embed(ctx)
        embed.title = "Coffee! ☕"
        try:
            embed.set_image(url=response["file"])
        except KeyError:
            embed = self.make_error_embed(ctx)
            embed.description = "API error occurred! :cry:"
            await ctx.send(embed=embed)
        else:
            await ctx.message.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
