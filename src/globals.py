from .utils.bindings import *
from dotenv import load_dotenv
from os import getenv
load_dotenv()

'''
Global Wrappers/Managers:

These will be used via cogs and config files
to perform database connections in a unified
queue based call system
'''

global db, cache

db=DatabaseWrapper(getenv("DATABASE_URI"))
cache=CacheManger(int(getenv("CACHE_SIZE")))