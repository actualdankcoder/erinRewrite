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

    def make_embed(self, ctx: commands.Context) -> Embed:
        embed = Embed(color=ctx.message.author.color,
                      timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.message.author.display_name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_author(name=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url)
        return embed

    def make_error_embed(self, ctx: commands.Context) -> Embed:
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
    async def hug(self, ctx: commands.Context,
                  user: commands.Greedy[discord.Member] = None):
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
    async def laugh(self, ctx: commands.Context,
                    user: commands.Greedy[discord.Member] = None):
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

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="lick",
                      description="<a:lick:828297410458550322>")
    async def lick(self, ctx: commands.Context,
                   user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna lick in "
                                    f"the command ;)")
            return
        licked_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "*Tasty*"
        embed.description = f"{ctx.author.mention} just licked {licked_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/lick")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="cry",
                      description=":pensize: :(")
    async def cry(self, ctx: commands.Context):
        embed = self.make_embed(ctx)
        embed.title = "<a:KannaCry:822716843440734218>" * 3
        response = await self.api_call("http://api.nekos.fun:8080/api/cry")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="cuddle",
                      description="Cuddle someone "
                                  "<a:pandaheart:828307130914177024>")
    async def cuddle(self, ctx: commands.Context,
                     user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna cuddle with "
                                    f"in the command ;)")
            return
        cuddled_with = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "aww cuddles uwu"
        embed.description = f"{ctx.author.mention} just cuddled {cuddled_with}"
        response = await self.api_call("http://api.nekos.fun:8080/api/cuddle")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="kiss",
                      description="OwO kiss someone :flushed:")
    async def kiss(self, ctx: commands.Context,
                   user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna kiss in the "
                                    f"command ;)")
            return
        kissed_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "<a:nekokissr:820991965217816607>" * 2
        embed.description = f"{ctx.author.mention} just kissed {kissed_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/kiss")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="pat",
                      description="Pat someone <:worrypat:828215349710684170>")
    async def pat(self, ctx: commands.Context,
                  user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna pat in the "
                                    f"command ;)")
            return
        if user == ctx.author:
            await ctx.message.reply("Imagine patting yourself...")
            return
        patted_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "*cute pats*"
        embed.description = f"{ctx.author.mention} just patted {patted_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/pat")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="poke",
                      description="Poke people!!!")
    async def poke(self, ctx: commands.Context,
                   user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna poke in the "
                                    f"command ;)")
            return
        if user == ctx.author:
            await ctx.message.reply("Imagine poking yourself...")
            return
        poked_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "***poke poke***"
        embed.description = f"{ctx.author.mention} just poked {poked_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/poke")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="baka",
                      description="BAKA!!!")
    async def baka(self, ctx: commands.Context,
                   user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply("Who's the baka??? (Mention it with the "
                                    "command)")
            return
        bakas = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "**BAKA!!!***"
        embed.description = f"{bakas}, ANTA BAKA?!?!?!?!?!?!"
        response = await self.api_call("http://api.nekos.fun:8080/api/baka")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="feed",
                      description="gib me food plz")
    async def feed(self, ctx: commands.Context,
                   user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply("Who are you feeding? (Mention it with "
                                    "the command)")
            return
        fed_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "Yummy"
        embed.description = f"{ctx.author.mention} fed {fed_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/feed")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="smug",
                      description="Smug moment "
                                  "<:Davie_Smug:773399926650175488>")
    async def smug(self, ctx: commands.Context):
        embed = self.make_embed(ctx)
        embed.title = f"{ctx.author.name} smugged"
        response = await self.api_call("http://api.nekos.fun:8080/api/smug")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="slap",
                      description="Bitch slap moment "
                                  "<:slap:500660862110138369>")
    async def slap(self, ctx: commands.Context,
                   user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna slap in the "
                                    f"command ;)")
            return
        if user == ctx.author:
            await ctx.message.reply("Imagine slapping yourself...")
            return
        slapped_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "**Ouch**"
        embed.description = f"{ctx.author.mention} just slapped " \
                            f"{slapped_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/slap")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(3, 5, BucketType.user)
    @commands.command(name="tickle",
                      description="Tickle someone!")
    async def tickle(self, ctx: commands.Context,
                     user: commands.Greedy[discord.Member] = None):
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna tickle in the "
                                    f"command ;)")
            return
        if user == ctx.author:
            await ctx.message.reply("Imagine tickling yourself...")
            return
        slapped_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "Tickle, tickle!"
        embed.description = f"{ctx.author.mention} tickled " \
                            f"{slapped_users}"
        response = await self.api_call("http://api.nekos.fun:8080/api/tickle")
        url = response["image"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Action(bot))
