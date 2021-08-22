"""
NSFW NSFW NSFW NSFW NSFW NSFW NSFW NSFW NSFW NSFW
"""

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
from src.utils.exceptions import *
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


class NSFW(ErinCog):
    """
    Meme commands <a:awkwardkid:843361776619618304>
    ~~There's a slight possibility that they aren't memes~~
    """

    async def api_call(self, url: str,
                       return_text: bool = False) -> Union[dict, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if return_text:
                    return await response.text()
                else:
                    return await response.json()

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="hentai", description="Juicy hentai")
    async def hentai(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Juicy hentai for you!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/Random_hentai_gif"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="erok", description="Erok kitsune")
    async def erok(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Erok Kitsune!!!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/erok"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="eroneko", description="ERONEKO")
    async def eroneko(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "***ERO*** NEKO!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/erokemo"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="feet", aliases=["feetgif", "foot"],
                      description="Feet")
    async def feet(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "***Feet***"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/feet"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="cum", description="Sticky white stuff")
    async def cum(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "***Sticky white stuff!***"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/cum"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="hthights", aliases=["hthigh", "animethigh",
                                                "anime_thigh", "htthigh",
                                                "hentaithigh", "hentai_thigh"],
                      description="Thic thighs!")
    async def hthighs(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Thic thights!"
        response = await self.api_call(
            "https://shiro.gg/api/images/nsfw/thighs"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="nekofuck", aliases=["neko_fuck", "nekosex",
                                                "neko_sex", "nekogif"],
                      description="Catgirls!")
    async def nekofuck(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Catgirls!!!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/nsfw_neko_gif"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="futanari", description="Futanari")
    async def futanari(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Futanari"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/futanari"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="boobs", aliases=["boob"], description="Tiddies!")
    async def boobs(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "**Tiddies**!!!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/boobs"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="blowjob", aliases=["bj"])
    async def blowjob(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Oh shit!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/blowjob"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="pussy", aliases=["vagina", "vaginas"])
    async def pussy(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Dang!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/pussy"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="spank", description="Oooof!")
    async def spank(self, ctx: commands.Context, user: commands.Greedy[discord.Member] = None):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("this command can only be used in a NSFW "
                                    "channel.")
            return
        if user is None:
            await ctx.message.reply(f"Mention someone you wanna spank in the "
                                    f"command ;)")
            return
        spanked_users = "".join(f"{users.mention} " for users in user)
        embed = self.make_embed(ctx)
        embed.title = "Oooof!"
        embed.description = f"{ctx.author.mention} spanked {spanked_users}"
        response = await self.api_call("https://nekos.life/api/v2/img/spank")
        url = response["url"]
        embed.set_image(url=url)
        await ctx.send(" ".join([users.mention for users in user]),
                       embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="lesbian", aliases=["les"])
    async def lesbian(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/les"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="trap")
    async def trap(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/trap"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="hololewd", aliases=["holo_lewd"])
    async def hololewd(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/hololewd"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="neko", aliases=["nekos"],
                      description="Neko!!!")
    async def neko(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Neko!!!"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/ngif"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="foxgirl",
                      aliases=["fox_girl", "foxgirls", "fox_girls"])
    async def foxgirl(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        embed.title = "Foxgirl for you:"
        response = await self.api_call(
            "https://nekos.life/api/v2/img/fox_girl"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="lewdkitsune",
                      aliases=["lewd_kitsune", "lewdk", "lewd_k"])
    async def lewdkitsune(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/lewdk"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="kuni")
    async def kuni(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/kuni"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="femdom")
    async def femdom(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/femdom"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="erofeet")
    async def erofeet(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/erofeet"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="solo")
    async def solo(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/solog"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="gasm", aliases=["orgasm", "orgy"])
    async def gasm(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/gasm"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="anal")
    async def anal(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/anal"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="wallpaper", aliases=["wl"])
    async def wallpaper(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekos.life/api/v2/img/wallpaper"
        )
        url = response["url"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="ass", aliases=["hentaiass", "hentai_ass", "hass"])
    async def ass(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekobot.xyz/api/image?type=hass"
        )
        url = response["message"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="porn", aliases=["pgif"])
    async def porn(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekobot.xyz/api/image?type=pgif"
        )
        url = response["message"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="4k", aliases=["fourk", "four_k"])
    async def fourk(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekobot.xyz/api/image?type=4k"
        )
        url = response["message"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="yaoi")
    async def yaoi(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekobot.xyz/api/image?type=yaoi"
        )
        url = response["message"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 7, BucketType.user)
    @commands.command(name="thigh", aliases=["thighs"])
    async def thigh(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.message.reply("This command can only be used in a NSFW "
                                    "channel.")
            return
        embed = self.make_embed(ctx)
        response = await self.api_call(
            "https://nekobot.xyz/api/image?type=thigh"
        )
        url = response["message"]
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
