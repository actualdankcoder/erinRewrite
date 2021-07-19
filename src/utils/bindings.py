import logging
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from src.utils.cacher import CacheManger
from src.utils.create_logger import create_logger
from src.utils.singleton import Singleton
from src.utils.exceptions import *
from string import ascii_letters, digits, punctuation

# Configure logger
logger = create_logger(name=__file__, level=logging.DEBUG)

# Define a gazillion constants
MAX_PREFIX_LENGTH = 1
MIN_PREFIX_LENGTH = 1

MAX_PREFIXES_PER_GUILD = 3
MIN_PREFIXES_PER_GUILD = 1

ALLOWED_PREFIXES = list(ascii_letters + digits + punctuation)


def get_blank_user_template() -> dict:
    user_template = {
        "id": None
    }
    return user_template.copy()


def get_blank_guild_template() -> dict:
    guild_template = {
        "id": None,
        "prefixes": ["-", "x"]
    }
    return guild_template.copy()


class AsyncErinDatabase(metaclass=Singleton):
    """
    Responsible for making database requests across all cogs
    (AsyncErinDatabase is a singleton so you can instantiate in each cog
    and it won't create more connections)
    """

    def __init__(self, URI: str):
        logger.debug("Starting MongoDB connection")
        self.database = AsyncIOMotorClient(URI)
        self.erin_db = self.database.erin_rewrite
        self.users_col = self.erin_db["users"]
        self.guild_col = self.erin_db["guilds"]
        self.cache_manager = CacheManger()

    async def get_user(self, user_id: str) -> dict:
        callback = await self.users_col.find_one({"id": user_id})
        if callback is None:
            doc = get_blank_user_template()
            doc["id"] = user_id
            await self.users_col.insert_one(doc)
            logger.debug(f"User ID {user_id} has been registered!")
            return doc
        else:
            return callback

    async def set_user(self, user_id: str, new_doc: dict):
        await self.users_col.replace_one({"id": user_id}, new_doc,
                                         upsert=True)

    async def get_guild(self, guild_id: str) -> dict:
        callback = await self.guild_col.find_one({"id": guild_id})
        if callback is None:
            doc = get_blank_guild_template()
            doc["id"] = guild_id
            await self.guild_col.insert_one(doc)
            logger.debug(f"Guild ID {guild_id} has been registered!")
            return doc
        else:
            return callback

    async def set_guild(self, guild_id: str, new_doc: dict):
        await self.guild_col.replace_one({"id": guild_id}, new_doc,
                                         upsert=True)

    async def get_prefix(self, guild_id: int) -> List[str]:
        return (await self.get_guild(str(guild_id)))["prefixes"]

    async def add_prefix(self, guild_id: int, new_prefix: str):
        guild = await self.get_guild(str(guild_id))
        prefixes = guild["prefixes"]
        if len(new_prefix) > MAX_PREFIX_LENGTH:
            raise TooLongPrefix(f"The prefix \"{new_prefix}\" is too long! "
                                f"(the prefix must be less then or equal to"
                                f"{MAX_PREFIX_LENGTH} character(s))")
        if len(new_prefix) < MIN_PREFIX_LENGTH:
            raise TooShortPrefix(f"The prefix \"{new_prefix}\" is too short! "
                                 f"(the prefix must be greater then or equal "
                                 f"to {MIN_PREFIX_LENGTH} character(s))")
        if new_prefix in prefixes:
            raise PrefixAlreadyExists(f"The prefix \"{new_prefix}\" already "
                                      f"exists!")
        for char in new_prefix:
            if char not in ALLOWED_PREFIXES:
                raise InvalidPrefix(f"The character \"{char}\" (in "
                                    f"\"{new_prefix}\") is not a valid "
                                    f"character for a prefix!")
        if len(prefixes) + 1 > MAX_PREFIXES_PER_GUILD:
            raise TooManyPrefixes(f"You are already at the maximum amount "
                                  f"({MAX_PREFIXES_PER_GUILD}) of prefixes!")
        prefixes.append(new_prefix)
        guild["prefixes"] = prefixes
        await self.set_guild(str(guild_id), guild)

    async def remove_prefix(self, guild_id: int, old_prefix: str):
        guild = await self.get_guild(str(guild_id))
        prefixes = guild["prefixes"]
        if old_prefix not in prefixes:
            raise PrefixDoesNotExist(f"The prefix \"{old_prefix}\" isn't an "
                                     f"existing prefix!")
        if len(prefixes) - 1 > MIN_PREFIXES_PER_GUILD:
            raise TooManyPrefixes(f"You are already at the minimum amount "
                                  f"({MIN_PREFIXES_PER_GUILD}) of prefixes!")
        prefixes.pop(prefixes.index(old_prefix))
        guild["prefixes"] = prefixes
        await self.set_guild(str(guild_id), guild)
