import logging
from json import loads as load_json
from os import getenv
from pathlib import Path
from random import randint
from typing import Union

import aiohttp
from discord import Embed, HTTPException
from discord.ext import commands
from discord.ext.commands import BucketType
from dotenv import load_dotenv

from src.utils.bindings import AsyncErinDatabase
from src.utils.create_logger import create_logger
from src.utils.ErinCog import ErinCog

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


class Fun(ErinCog):
    """
    What fun this category possess
    """

    async def api_call(self, url: str,
                       return_text: bool = False) -> Union[dict, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if return_text:
                    return await response.text()
                else:
                    return await response.json()

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="furrify", aliases=["furry", "uwu", "uwuify",
                                               "owo", "owoify"],
                      description="Makes youw text fuwwy uwu")
    async def furrify(self, ctx: commands.Context, msg: str = ""):
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
        uwu_text = response["owo"]
        await ctx.send(uwu_text)

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="8ball", aliases=["8_ball", "ball", "eightball",
                                             "eight_ball"],
                      description="Let the magic 8ball decide your fate 😈")
    async def ball(self, ctx: commands.Context, question: str = ""):
        embed = self.make_error_embed(ctx)
        if len(question) == 0:
            embed.description = "No question was provided!"
            await ctx.send(embed=embed)
            return
        embed = self.make_embed(ctx)
        response = await self.api_call("https://nekos.life/api/v2/8ball")
        embed.title = "8ball 🎱"
        embed.description = response["response"]
        embed.set_thumbnail(url=response["url"])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 3, BucketType.user)
    @commands.command(name="coffee",
                      description="Shows a picture of coffee :smirk:")
    async def coffee(self, ctx):
        response = await self.api_call("https://coffee.alexflipnote.dev/random.json")
        embed = self.make_embed(ctx)
        embed.title = "Coffee! ☕"
        embed.set_image(url=response["file"])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(name="randomname", aliases=["random_name"],
                      description="Random name generator")
    async def random_name(self, ctx):
        response = await self.api_call("https://nekos.life/api/v2/name")
        rand_name = response["name"]
        await ctx.message.reply(rand_name)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="quote", description="Sends a quote")
    async def quote(self, ctx):
        quotes = load_json(
            await self.api_call("https://type.fit/api/quotes",
                                return_text=True)
        )
        num = randint(1, len(quotes))
        content = quotes[num]["text"]
        author = quotes[num]["author"]
        await ctx.message.reply(f"\"{content}\" - {author}")

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(name="cat", aliases=["meow", "simba", "cats"],
                      description="Cats!!! ~~dogs are better~~")
    async def cat(self, ctx):
        response = await self.api_call("http://aws.random.cat/meow")
        embed = self.make_embed(ctx)
        embed.title = "Catto!"
        embed.set_image(url=response["file"])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(name="advice", description="Gives you some advice! "
                                                 ":heart:")
    async def advice(self, ctx):
        response = await self.api_call("https://api.adviceslip.com/advice",
                                       return_text=True)
        response = load_json(response)
        advice = response["slip"]["advice"]
        await ctx.message.reply(advice)

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(name="mock", description="mOcK SoME tEXt")
    async def mock(self, ctx: commands.Context, msg: str = ""):
        embed = self.make_error_embed(ctx)
        if len(msg) == 0:
            embed.description = "Please pass in some text!"
            await ctx.send(embed=embed)
            return
        banned = ["@here", "@everyone", "<@&", "<@!"]
        for word in banned:
            if word in msg:
                embed.description = "You can't ping with this command!"
                await ctx.send(embed=embed)
                return

        def even_rand_bool():
            last_true = 0
            while True:
                val = True if randint(min(last_true, 9), 10) > 5 else False
                if val:
                    last_true = 0
                else:
                    last_true += 1
                yield val

        new_msg = ""
        for char in msg:
            new_msg += char.upper() if next(even_rand_bool()) else char.lower()
        await ctx.message.reply(new_msg)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="fact", description="Sends a fact")
    async def fact(self, ctx):
        response = await self.api_call("https://nekos.life/api/v2/fact")
        fact = response["fact"]
        return await ctx.message.reply(fact)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="goose", aliases=["geese"],
                      description="Shows a picture of some geese")
    async def goose(self, ctx):
        embed = self.make_embed(ctx)
        response = await self.api_call("https://nekos.life/api/v2/img/goose")
        url = response["url"]
        embed.title = "Geese!"
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(3, 7, BucketType.user)
    @commands.command(name="waifu", description="Generates waifus")
    async def waifu(self, ctx):
        embed = self.make_embed(ctx)
        response = await self.api_call("https://nekos.life/api/v2/img/waifu")
        url = response["url"]
        embed.title = "Here's a waifu for you:"
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
