"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Base class for ROR API client.
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import Coroutine, Generic, List, Optional, TypeVar, Union

import httpx

from rorclient.config import config
from rorclient.models import Institution

T = TypeVar("T")


class BaseRORClient:
    """
    Base class for ROR clients, encapsulating shared logic.
    """

    _ror_id_pattern = re.compile(r"^0[a-z|0-9]{6}[0-9]{2}$")
    _ror_id_pattern_strict = re.compile(r"^0[a-hj-km-np-tv-z|0-9]{6}[0-9]{2}$")

    def __init__(
        self, prefetch_relationships: bool = False, max_depth: int = 2
    ) -> None:
        """Initializes the shared attributes."""
        self.prefetch_relationships = prefetch_relationships
        self.max_depth = max_depth
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "RORClient https://github.com/ADernild/RORClient",
        }

    def _initialize_client(
        self, client: Union[httpx.Client, httpx.AsyncClient]
    ) -> None:
        """Initializes the HTTP client with shared configuration."""
        client.base_url = str(config.base_url)
        client.headers.update(self.headers)

    def _validate_ror_id(self, ror_id: str) -> None:
        """Validates a single ROR ID."""
        if not ror_id:
            raise ValueError("ror_id cannot be None or empty")

        extracted_ror_id = self._extract_ror_id(ror_id)

        # Check if the ROR ID matches the pattern
        if not self._ror_id_pattern.match(extracted_ror_id):
            raise ValueError(f"Invalid ROR ID format: {ror_id}")

    def _validate_ror_ids(self, ror_ids: List[str]) -> None:
        """Validates the list of ROR IDs."""
        if not ror_ids:
            raise ValueError("ror_ids cannot be empty")

        for ror_id in ror_ids:
            self._validate_ror_id(ror_id)

    def _validate_ror_id_strict(self, ror_id: str) -> None:
        """Validates a single ROR ID with stricter rules."""
        if not ror_id:
            raise ValueError("ror_id cannot be None or empty")

        extracted_ror_id = self._extract_ror_id(ror_id)

        # Check if the ROR ID matches the strict pattern
        if not self._ror_id_pattern_strict.match(extracted_ror_id):
            raise ValueError(f"Invalid ROR ID format: {ror_id}")

    def _validate_ror_ids_strict(self, ror_ids: List[str]) -> None:
        """Validates a list of ROR IDs with stricter rules."""
        if not ror_ids:
            raise ValueError("ror_ids cannot be empty")

        for ror_id in ror_ids:
            self._validate_ror_id_strict(ror_id)

    def _extract_ror_id(self, ror_id: str) -> str:
        """Extracts the unique portion of the ROR ID from a URL or returns the input if it's already a valid portion."""
        # Check if the input is a full URL
        url_pattern = re.compile(r"^https?://ror\.org/([0-9a-z|]+)$")
        match = url_pattern.match(ror_id)

        if match:
            return match.group(1)

        # If it's not a URL, assume it's the unique portion
        return ror_id

    def _process_institution_data(self, institution_data: dict, depth: int) -> dict:
        """Processes institution data to prefetch relationships if needed."""
        if self.prefetch_relationships and depth < self.max_depth:
            institution_data["relationships"] = [
                {
                    **rel,
                    "record": self.get_institution(rel["id"].split("/")[-1], depth + 1),
                }
                for rel in institution_data["relationships"]
            ]
        return institution_data

    @abstractmethod
    def get_institution(
        self, ror_id: str, depth: int = 0
    ) -> Union[T, Coroutine[None, None, T]]:
        """Abstract method to fetch a single institution by its ROR ID."""
        pass
