import json
from typing import Dict
import asyncio


async def async_str_to_dict(s: str, retries: int = 3) -> Dict:
    """
    Asynchronously converts a JSON-formatted string to a dictionary.

    Args:
        s (str): The JSON string to be converted.
        retries (int): The number of times to retry parsing the string in case of a JSONDecodeError. Default is 3.

    Returns:
        Dict: The parsed dictionary from the JSON string.

    Raises:
        json.JSONDecodeError: If the string cannot be parsed into a dictionary after the specified number of retries.
    """
    for attempt in range(retries):
        try:
            # Run json.loads directly since it's fast enough
            return json.loads(s)
        except json.JSONDecodeError as e:
            if attempt < retries - 1:
                continue  # Retry on failure
            else:
                raise e  # Raise the error if all retries fail


def str_to_dict(s: str, retries: int = 3) -> Dict:
    """
    Converts a JSON string to dictionary, handling both sync and async contexts.

    Args:
        s (str): The JSON string to be converted.
        retries (int): The number of times to retry parsing the string in case of a JSONDecodeError. Default is 3.

    Returns:
        Dict: The parsed dictionary from the JSON string.
    """
    # For simplicity and reliability, just try to parse the JSON directly first
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # If direct parsing fails, try the async path
        try:
            return async_str_to_dict(s, retries).__await__()
        except (AttributeError, RuntimeError):
            # If we can't await (not in async context), use run
            return asyncio.run(async_str_to_dict(s, retries))
