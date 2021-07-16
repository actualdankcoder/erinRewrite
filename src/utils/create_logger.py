"""
A module that creates a simple logger and returns it.
"""

import logging
import coloredlogs


DEFAULT_FORMAT = "%(asctime)s,%(msecs)03d %(hostname)s " \
                 "%(name)s[%(process)d] %(levelname)s %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def create_logger(name: str, level: int = logging.INFO,
                  use_color: bool = True) -> logging.Logger:
    logger = logging.getLogger(name=name)
    if use_color:
        coloredlogs.install(logger=logger, name=name, level=level,
                            fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=level)
        console_formatter = logging.Formatter(fmt=DEFAULT_FORMAT,
                                              datefmt=DEFAULT_DATE_FORMAT)
        console_handler.setFormatter(fmt=console_formatter)
        console_handler.setLevel(level=level)
        logger.propagate = False
        if console_handler not in logger.handlers:
            logger.addHandler(hdlr=console_handler)
        logger.setLevel(level=level)
    logger.debug(f"Created logger named {repr(name)} with level {repr(level)}")
    logger.debug(f"Handlers for {repr(name)}: {repr(logger.handlers)}")
    return logger
