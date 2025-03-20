"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Asynchronous client for interacting with the ROR API.
"""

import asyncio
import logging
from typing import ClassVar, List, Optional

import backoff
import httpx
from pydantic import BaseModel, PrivateAttr

from rorclient.base import BaseRORClient
from rorclient.config import config
from rorclient.models import Institution
from rorclient.utils import retry_with_backoff

logger = logging.getLogger(__name__)


class AsyncRORClient(BaseRORClient):
    """
    An asynchronous client for interacting with the Research Organization Registry (ROR) API.

    The RORClient provides methods to fetch institutions by their ROR ID, fetch multiple institutions,
    and search for institutions. The client can also prefetch relationships between institutions up to a specified depth.
    """

    def __init__(
        self, prefetch_relationships: bool = False, max_depth: int = 2
    ) -> None:
        """Initializes the HTTPX client for connection reuse."""
        super().__init__(prefetch_relationships, max_depth)
        self._client = httpx.AsyncClient()
        self._initialize_client(self._client)

    async def __aenter__(self):
        """Allows the client to be used as an async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensures the HTTPX async client is closed when exiting context."""
        await self._client.aclose()

    @retry_with_backoff()
    async def get_institution(
        self, ror_id: str, depth: int = 0
    ) -> Optional[Institution]:
        """
        Fetches a single institution by its ROR ID asynchronously.

        Args:
            ror_id (str): The ROR ID of the institution.

        Returns:
            Optional[Institution]: An Institution object if found, otherwise None.

        Raises:
            ValueError: If the response status code is unexpected.
        """
        self._validate_ror_id(ror_id)

        logger.debug(f"Fetching institution with ROR ID: {ror_id}")
        response = await self._client.get(f"organizations/{ror_id}")

        if response.status_code == 200:
            institution_data = await response.json()
            institution_data = self._process_institution_data(institution_data, depth)
            return Institution(**institution_data)
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Unexpected response: {response.status_code}")

    @retry_with_backoff()
    async def get_multiple_institutions(self, ror_ids: List[str]) -> List[Institution]:
        """
        Fetches multiple institutions by their ROR IDs asynchronously.

        Args:
            ror_ids (List[str]): A list of ROR ID strings.

        Returns:
            List[Institution]: A list of Institution objects.

        Raises:
            ValueError: If the IDs list is empty.
        """
        self._validate_ror_ids(ror_ids)

        logger.debug(f"Fetching multiple institutions: {ror_ids}")

        tasks = [self.get_institution(ror_id) for ror_id in ror_ids]
        results = await asyncio.gather(*tasks)

        return [result for result in results if result is not None]

    async def close(self):
        """Closes the HTTPX async client."""
        await self._client.aclose()
