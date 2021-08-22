import logging
from os import getenv
from pathlib import Path

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
            user = [ctx.author]
        embed.description = ""
        for users in user:
            user_doc = await erin_db.get_user(str(users.id))
            user_balance = user_doc["balance"]
            embed.description += f"{users.mention} has {user_balance} {CURRENCY_NAME}\n"
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
