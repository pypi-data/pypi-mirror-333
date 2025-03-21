"""Utility functions"""

from collections.abc import Mapping
from functools import reduce


def deep_get(dictionary, keys, default=None):
    """
    Get a value from a nested dictionary using a dot-separated key string.

    Args:
        dictionary (dict): The dictionary to search.
        keys (str): A dot-separated string of keys to search for. e.g. 'a.b.c'
        default (Any, optional): The default value to return if the key is not found.
    """
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, Mapping) else default,
        keys.split('.'),
        dictionary,
    )
