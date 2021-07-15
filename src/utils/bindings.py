from asyncio.tasks import Task
import motor.motor_asyncio
import asyncio
from lru import LRU
from discord.ext import tasks, commands
class CacheManger:
    '''
        Responsible for caching

    '''
    def __init__(self, cache_size):
        self.cache=LRU(cache_size)
        pass


class DatabaseWrapper:
    '''
        Responsible for making database requests across all cogs,
        An Instance of this class would be globally accessible via globals.py
    
    '''
    def __init__(self, URI):
        self.database=motor.motor_asyncio.AsyncIOMotorCLient(URI)
        self.economy=self.database["economy"]
        self.cooldowns=self.database["cooldowns"]
        self.queue=asyncio.Queue()

    async def __new_task(self, task):
        '''
            Add tasks to queue flow, a background task
            would be responsible for executing these 
            at set intervals of time
        '''
        await self.queue.put(task)

    @tasks.loop(seconds=5)
    async def task_loader(self):
        '''
            This task loader is responsible
            to make database calls for the given jobs
        '''
        task=await self.queue.get()
