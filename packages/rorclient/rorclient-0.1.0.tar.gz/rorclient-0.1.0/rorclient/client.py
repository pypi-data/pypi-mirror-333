"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Synchronous client for interacting with the ROR API.
"""

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


class RORClient(BaseRORClient):
    """
    A synchronous client for interacting with the Research Organization Registry (ROR) API.

    The RORClient provides methods to fetch institutions by their ROR ID, fetch multiple institutions,
    and search for institutions. The client can also prefetch relationships between institutions up to a specified depth.
    """

    def __init__(
        self, prefetch_relationships: bool = False, max_depth: int = 2
    ) -> None:
        """Initializes the HTTPX client for connection reuse."""
        super().__init__(prefetch_relationships, max_depth)
        self._client = httpx.Client()
        self._initialize_client(self._client)

    def __enter__(self):
        """Allows the client to be used as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the HTTPX client is closed when exiting context."""
        self._client.close()

    @retry_with_backoff()
    def get_institution(self, ror_id: str, depth: int = 0) -> Optional[Institution]:
        """
        Fetches a single institution by its ROR ID.

        Args:
            ror_id (str): The ROR ID of the institution.
            depth (int): Current depth of recursion for prefetching relationships.

        Returns:
            Optional[Institution]: An Institution object if found, otherwise None.

        Raises:
            ValueError: If the ID is None or the response status code is unexpected.
        """
        self._validate_ror_id(ror_id)

        logger.debug(f"Fetching institution with ROR ID: {ror_id}")
        response = self._client.get(f"organizations/{ror_id}")

        if response.status_code == 200:
            institution_data = response.json()
            institution_data = self._process_institution_data(institution_data, depth)
            return Institution(**institution_data)
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Got {response.status_code} from ROR")

    @retry_with_backoff()
    def get_multiple_institutions(self, ror_ids: List[str]) -> List[Institution]:
        """
        Fetches multiple institutions by their ROR IDs.

        Args:
            ror_ids (List[str]): A list of ROR ID strings.

        Returns:
            List[Institution]: A list of Institution objects.

        Raises:
            ValueError: If the IDs list is empty.
        """

        self._validate_ror_ids(ror_ids)
        logger.debug(f"Fetching multiple institutions: {ror_ids}")
        institutions = []
        for ror_id in ror_ids:
            institution = self.get_institution(ror_id)
            if institution:
                institutions.append(institution)

        return institutions

    def close(self):
        """Closes the HTTPX client."""
        self._client.close()
