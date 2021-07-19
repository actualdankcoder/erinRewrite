import logging

from lru import LRU

from src.utils.create_logger import create_logger

# Configure logger
logger = create_logger(name=__file__, level=logging.DEBUG)


class CacheManger:
    """
    Responsible for caching
    """

    def __init__(self, cache_size: int = 1000):
        logger.debug("Initializing cache...")
        self.prefix_cache = LRU(cache_size)
