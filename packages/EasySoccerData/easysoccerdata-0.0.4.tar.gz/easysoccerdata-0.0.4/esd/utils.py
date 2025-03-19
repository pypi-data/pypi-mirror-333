"""
This module contains utility functions that are used in the project.
"""

import re
import time
import httpx


def get_today() -> str:
    """
    Get the current date in the format "YYYY-MM-DD".

    Returns:
        str: The current date in the format "YYYY-MM-DD".
    """
    return time.strftime("%Y-%m-%d")


def camel_to_snake(name: str) -> str:
    """
    Convert a camel case string to a snake case string.

    Args:
        name (str): The camel case string.

    Returns:
        str: The snake case string.
    """
    return re.sub(
        r"([a-z0-9])([A-Z])", r"\1_\2", re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    ).lower()


def get_json(url: str) -> dict:
    """
    Get the JSON response from the given URL.

    Args:
        url (str): The URL to get the JSON response.

    Returns:
        dict: The JSON response.
    """
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return {}
        raise exc
