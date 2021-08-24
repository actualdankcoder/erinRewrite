import logging
from os import getenv
from random import randint
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

BET_COIN_FLIP_CHANCE = 40
BET_COIN_FLIP_REWARD = 1.75
BET_DICE_ROLL_CHANCE = 10
BET_DICE_ROLL_REWARD = 2.5


def random_chance(chance: int) -> bool:
    assert chance >= 0 and chance <= 100
    return randint(1, 100) <= chance


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
        await ctx.message.reply(embed=embed)

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
        await ctx.message.reply(embed=embed)

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
        await ctx.message.reply(embed=embed)

    @commands.cooldown(5, 10, BucketType.user)
    @commands.command(name="betcoinflip", aliases=["bet_coin_flip", "betflip",
                                                   "bet_flip", "coinflip",
                                                   "coin_flip", "betcoin",
                                                   "bet_coin", "bcf", "bf"],
                      description=f"Bet some {CURRENCY_NAME} on a coin flip!")
    async def bet_coin_flip(self, ctx: commands.Context, amount: int,
                            side: str):
        user_doc = await erin_db.get_user(str(ctx.author.id))
        user_balance = user_doc["balance"]
        if amount < 1:
            embed = self.make_error_embed(ctx)
            embed.title = ""
            embed.description = f"{ctx.author.mention} you cannot bet " \
                                f"less then 1 {CURRENCY_NAME}!"
            await ctx.message.reply(embed=embed)
            return
        elif amount > user_balance:
            embed = self.make_error_embed(ctx)
            embed.title = ""
            embed.description = f"{ctx.author.mention} you cannot bet more " \
                                f"then you have!"
            await ctx.message.reply(embed=embed)
            return
        else:
            embed = self.make_embed(ctx)
            side = side.replace(" ", "").lower()
            if side in ("heads", "h"):
                side = "heads"
            elif side in ("tails", "t"):
                side = "tails"
            else:
                raise commands.errors.BadArgument("side is not either "
                                                  "\"heads\" or \"tails\"!")
            if random_chance(BET_COIN_FLIP_CHANCE):
                reward = round(amount * BET_COIN_FLIP_REWARD)
                user_doc["balance"] += reward
                embed.description = f"{ctx.author.mention} it was {side}! " \
                                    f"You win {reward} {CURRENCY_NAME}."
            else:
                user_doc["balance"] -= amount
                embed.description = f"{ctx.author.mention} better luck next " \
                                    f"time - it was " \
                                    f"{'tails' if side == 'heads' else 'heads'}"
            await erin_db.set_user(str(ctx.author.id), user_doc)
            await ctx.message.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
