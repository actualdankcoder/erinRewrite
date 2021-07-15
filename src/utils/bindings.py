import asyncio

import motor.motor_asyncio
from discord.ext import tasks
from lru import LRU

from singleton import Singleton
from task import *


class CacheManger:
    """
    Responsible for caching
    """

    def __init__(self, cache_size: int = 1000):
        self.cache = LRU(cache_size)


class ErinDatabase(metaclass=Singleton):
    """
    Responsible for making database requests across all cogs
    An instance of this class would be globally accessible via src/globals.py
    """

    def __init__(self, URI: str):
        self.database = motor.motor_asyncio.AsyncIOMotorCLient(URI)
        self.economy = self.database["economy"]
        self.cooldowns = self.database["cooldowns"]
        self.queue = asyncio.Queue()
        self.cache = CacheManger()

    async def new_task(self, task: Task):
        """
        Add tasks to queue flow, a background task would be responsible for
        executing these at set intervals of time
        """
        await self.queue.put(task)

    @tasks.loop(seconds=0.5)
    async def task_loader(self):
        """
        This task loader is responsible for making database calls for the given
        jobs
        """
        task = await self.queue.get()
