import logging
from os import getenv
from pathlib import Path

import arrow
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.bindings import ErinDatabase
from utils.create_logger import create_logger

from typing import List
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
        logger.error(f"Could not find {repr(var_name)} in environment variables!")
        raise ValueError(f"Could not find {repr(var_name)} in environment variables!")
    return var


# Load environment variables
token = load_env_var("BOT_TOKEN")
db_uri = load_env_var("DATABASE_URI")

# Create connection to database
erin_db = ErinDatabase(URI=db_uri)


def get_prefix(client, message) -> List[str]:
    return erin_db.get_prefix(message.guild.id)


class ErinBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=get_prefix, intents=intents,
                         guild_subscriptions=True, case_insensitive=True)
        self.remove_command("help")
        self.startup_time = arrow.utcnow()


erin = ErinBot()

# Load extensions
logger.info("Loading extensions...")
cog_path = Path(__file__).parent / "cogs"
logger.debug(f"Path to cogs is {cog_path}")
assert cog_path.exists() and cog_path.is_dir()
for file in cog_path.iterdir():
    if file.suffix == ".py" and not file.name.startswith("_"):
        erin.load_extension(f"cogs.{file.stem}")
logger.debug(f"Loaded {len(list(cog_path.iterdir()))} cog(s)")

logger.info("Running bot")
erin.run(token)
