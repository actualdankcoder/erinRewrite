import logging
from typing import List

from lru import LRU
from pymongo import MongoClient

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


class ErinDatabase(metaclass=Singleton):
    """
    Responsible for making database requests across all cogs
    (ErinDatabase is a singleton so you can instantiate in each cog
    and it won't create more connections)
    """

    def __init__(self, URI: str):
        logger.debug("Starting MongoDB connection")
        self.database = MongoClient(URI)
        self.erin_db = self.database.erin_rewrite
        self.users_col = self.erin_db["users"]
        self.guild_col = self.erin_db["guilds"]
        self.cache_manager = CacheManger()

    def register_user_if_needed(self, user_id: int):
        user_id = str(user_id)
        if self.users_col.find_one({"id": user_id}) is None:
            doc = get_blank_user_template()
            doc["id"] = user_id
            self.users_col.insert_one(doc)
            logger.debug(f"User ID {user_id} has been registered!")

    def register_guild_if_needed(self, guild_id: int):
        guild_id = str(guild_id)

        # Verify if the guild prefix was cached before
        if self.cache_manager.prefix_cache.has_key(guild_id):
            return self.cache_manager.prefix_cache[guild_id]

        if self.guild_col.find_one({"id": guild_id}) is None:
            doc = get_blank_guild_template()
            doc["id"] = guild_id
            self.guild_col.insert_one(doc)
            self.cache_manager.prefix_cache[guild_id]=doc["prefixes"]
            logger.debug(f"Guild ID {guild_id} has been registered!")
            return doc["prefixes"]

    def get_prefix(self, guild_id: int) -> List[str]:
        
        return self.register_guild_if_needed(guild_id)
