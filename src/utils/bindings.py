import asyncio
from enum import Enum
from typing import Union

from lru import LRU
from motor.motor_asyncio import AsyncIOMotorClient

from singleton import Singleton


class CacheManger:
    """
    Responsible for caching
    """

    def __init__(self, cache_size: int = 1000):
        self.cache = LRU(cache_size)


class UserKeys(Enum):
    pass


def get_blank_user_template() -> dict:
    user_template = {

    }
    return user_template.copy()


class GuildKeys(Enum):
    PREFIXES = "prefixes"


def get_blank_guild_template() -> dict:
    guild_template = {
        GuildKeys.PREFIXES: ["-"]
    }
    return guild_template.copy()


class AsyncErinDatabase(metaclass=Singleton):
    """
    Responsible for making database requests across all cogs
    (AsyncErinDatabase is a singleton so you can instantiate in each cog
    and it won't create more connections)
    """

    def __init__(self, URI: str):
        self.database = AsyncIOMotorClient(URI)
        self.erin_db = self.database["erin_rewrite"]
        self.users_col = self.erin_db["users"]
        self.guild_col = self.erin_db["guilds"]
        self.task_queue = asyncio.Queue()
        self.cache = CacheManger()

    async def register_user_if_needed(self, user_id: Union[int, str]):
        if await self.users_col.find_one(str(user_id)) is None:
            await self.users_col.insert_one(get_blank_user_template())

    async def register_guild_if_needed(self, guild_id: Union[int, str]):
        if await self.guild_col.find_one(str(guild_id)) is None:
            await self.guild_col.insert_one(get_blank_guild_template())

    async def get_prefix(self, guild_id: Union[int, str]) -> list[str]:
        await self.register_guild_if_needed(guild_id)
        return self.guild_col.find_one(str(guild_id))[GuildKeys.PREFIXES]
