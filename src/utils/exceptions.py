class ErinError(Exception):
    """Un-specified error"""


class BadArguments(ErinError):
    """Passed in not-enough arguments"""


class TooManyPrefixes(ErinError):
    """Too many prefixes cause the max is 3"""
