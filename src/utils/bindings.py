import logging
from typing import List

from lru import LRU
from motor.motor_asyncio import AsyncIOMotorClient

from .create_logger import create_logger
from .singleton import Singleton

# Configure logger
logger = create_logger(name=__file__, level=logging.DEBUG)


class CacheManger:
    """
    Responsible for caching
    """

    def __init__(self, cache_size: int = 1000):
        self.prefix_cache = LRU(cache_size)


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

    async def get_prefix(self, guild_id: int) -> List[str]:
        return (await self.get_guild(str(guild_id)))["prefixes"]
