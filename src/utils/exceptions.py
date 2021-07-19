class ErinError(Exception):
    """Un-specified error"""


class PrefixError(ErinError):
    """An error that involves the prefix"""


class TooLongPrefix(PrefixError):
    """The prefix to be added is too long"""


class TooShortPrefix(PrefixError):
    """The prefix to be added is too short"""


class InvalidPrefix(PrefixError):
    """The prefix is an invalid character"""


class TooManyPrefixes(PrefixError):
    """Adding the prefix will put you over the limit of the maximum amount of
    prefixes"""


class TooLittlePrefixes(PrefixError):
    """Adding the prefix will put you under the limit of the minimum amount of
    prefixes"""


class PrefixAlreadyExists(PrefixError):
    """This prefix already exists"""


class PrefixDoesNotExist(PrefixError):
    """This prefix does not exist"""
