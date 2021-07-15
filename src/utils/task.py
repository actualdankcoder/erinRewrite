from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    """
    Represents all the types of tasks that can be executed
    """
    # Arguments:
    #   - The key "guild_id" with the value as the guild ID for the server
    #     you want to get the prefix for
    # Returns: A list of str which are the prefixes for that server
    # Raises: None
    GET_PREFIX = "get_prefix"
    # Arguments:
    #   - The key "guild_id" with the value as the guild ID for the server
    #     you want to add the prefix for
    #   - The key "add_prefix" with the value of the prefix you want to add
    # Returns: None
    # Raises: TooManyPrefixes when there are too many prefixes
    ADD_PREFIX = "add_prefix"
    # Arguments:
    #   - The key "guild_id" with the value as the guild ID for the server
    #     you want to remove the prefix for
    #   - The key "remove_prefix" with the value of the prefix you want to
    #     remove
    # Returns: None
    # Raises: None
    REMOVE_PREFIX = "remove_prefix"


@dataclass
class Task:
    """
    A single task, which is executed by the database wrapper and returned
    asynchronously
    """
    task_type: str
    arguments: dict = field(default_factory=dict)