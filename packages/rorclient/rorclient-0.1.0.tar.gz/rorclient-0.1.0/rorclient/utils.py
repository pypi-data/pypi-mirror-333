"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Utility functions for the RORClient package.
"""

import logging
from functools import wraps

import backoff
import httpx

from rorclient.config import config

logger = logging.getLogger(__name__)


def retry_with_backoff():
    """
    A custom decorator that wraps backoff.on_exception with logging.

    Args:
        max_time (int): The maximum amount of time to retry in seconds.

    Returns:
        A decorator that can be applied to functions to add retry logic with backoff.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return backoff.on_exception(
                backoff.expo,
                (httpx.RequestError, httpx.HTTPStatusError),
                max_tries=config.max_retries,
                max_time=config.max_retry_time,
                on_backoff=lambda details: logger.warning(
                    f"Backing off {details.get('wait', 'unknown')} seconds after {details.get('tries', 'unknown')} tries"
                ),
            )(func)(*args, **kwargs)

        return wrapper

    return decorator
