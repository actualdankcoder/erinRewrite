import logging
from os import getenv
from pathlib import Path

import arrow
import discord.ext.commands
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


CURRENCY_NAME = "Erin"

HOURLY_CLAIM = 100
DAILY_CLAIM = 1000
MONTHLY_CLAIM = 10_000


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


class Economy(ErinCog):
    """
    Economy commands
    """

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="balance", aliases=["bal", "$"],
                      description=f"Check how much {CURRENCY_NAME} you have!")
    async def balance(self, ctx: commands.Context,
                      user: commands.Greedy[discord.Member] = None):
        embed = self.make_embed(ctx)
        if user is None:
            user = ctx.author
        else:
            user = user[0]
        embed.description = ""
        user_doc = await erin_db.get_user(str(user.id))
        user_balance = user_doc["balance"]
        embed.description += f"{user.mention} has {user_balance} {CURRENCY_NAME}\n"
        await ctx.send(embed=embed)

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="hourly",
                      description=f"Claim some {CURRENCY_NAME} every hour!")
    async def hourly(self, ctx: commands.Context):
        user_doc = await erin_db.get_user(str(ctx.author.id))
        user_claims = user_doc["last_claim"]
        last_claim = user_claims["hourly"]
        one_hr_ago = arrow.utcnow().shift(hours=-1).timestamp()
        if one_hr_ago >= last_claim:
            user_doc["balance"] += HOURLY_CLAIM
            user_claims["hourly"] = arrow.utcnow().timestamp()
            await erin_db.set_user(str(ctx.author.id), user_doc)
            embed = self.make_embed(ctx)
            embed.description = f"{ctx.author.mention} you claimed your " \
                                f"hourly and got " \
                                f"{HOURLY_CLAIM} {CURRENCY_NAME}! You can " \
                                f"claim again in 1 hour."
        else:
            embed = self.make_error_embed(ctx)
            embed.title = ""
            can_get_in = arrow.get(last_claim).shift(hours=1)
            embed.description = f"{ctx.author.mention} you already claimed " \
                                f"your hourly reward. You can get it again " \
                                f"in {can_get_in.humanize(only_distance=True)}"
        await ctx.send(embed=embed)

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="daily",
                      description=f"Claim some {CURRENCY_NAME} every day!")
    async def daily(self, ctx: commands.Context):
        user_doc = await erin_db.get_user(str(ctx.author.id))
        user_claims = user_doc["last_claim"]
        last_claim = user_claims["daily"]
        one_day_ago = arrow.utcnow().shift(days=-1).timestamp()
        if one_day_ago >= last_claim:
            user_doc["balance"] += DAILY_CLAIM
            user_claims["daily"] = arrow.utcnow().timestamp()
            await erin_db.set_user(str(ctx.author.id), user_doc)
            embed = self.make_embed(ctx)
            embed.description = f"{ctx.author.mention} you claimed your " \
                                f"daily and got " \
                                f"{DAILY_CLAIM} {CURRENCY_NAME}! You can " \
                                f"claim again in 1 day."
        else:
            embed = self.make_error_embed(ctx)
            embed.title = ""
            can_get_in = arrow.get(last_claim).shift(days=1)
            embed.description = f"{ctx.author.mention} you already claimed " \
                                f"your daily reward. You can get it again " \
                                f"in {can_get_in.humanize(only_distance=True)}"
        await ctx.send(embed=embed)

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="monthly",
                      description=f"Claim some {CURRENCY_NAME} every month!")
    async def monthly(self, ctx: commands.Context):
        user_doc = await erin_db.get_user(str(ctx.author.id))
        user_claims = user_doc["last_claim"]
        last_claim = user_claims["monthly"]
        one_month_ago = arrow.utcnow().shift(days=-30).timestamp()
        if one_month_ago >= last_claim:
            user_doc["balance"] += MONTHLY_CLAIM
            user_claims["monthly"] = arrow.utcnow().timestamp()
            await erin_db.set_user(str(ctx.author.id), user_doc)
            embed = self.make_embed(ctx)
            embed.description = f"{ctx.author.mention} you claimed your " \
                                f"monthly and got " \
                                f"{MONTHLY_CLAIM} {CURRENCY_NAME}! You can " \
                                f"claim again in 30 days."
        else:
            embed = self.make_error_embed(ctx)
            embed.title = ""
            can_get_in = arrow.get(last_claim).shift(days=30)
            embed.description = f"{ctx.author.mention} you already claimed " \
                                f"your monthly reward. You can get it again " \
                                f"in {can_get_in.humanize(only_distance=True)}"
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
