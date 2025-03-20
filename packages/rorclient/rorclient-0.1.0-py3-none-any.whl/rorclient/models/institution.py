"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for institutions in the ROR API.
"""

from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from .admin import Admin
from .external_id import ExternalId
from .link import Link
from .location import Location
from .name import Name
from .relationship import Relationship


class Institution(BaseModel):
    """
    A model representing an institution in the ROR API.

    Attributes:
        admin (Admin): Administrative information about the record.
        domains (List[str]): The domains registered to the institution.
        established (Optional[int]): The year the institution was established.
        external_ids (List[ExternalId]): Other identifiers for the institution.
        id (HttpUrl): The unique ROR ID of the institution.
        links (List[Link]): The institution's website and Wikipedia page.
        locations (List[Location]): The locations of the institution.
        names (List[Name]): The names the institution goes by.
        relationships (List[Relationship]): Related organizations in ROR.
        status (str): The status of the institution (e.g., active, inactive, withdrawn).
        types (List[str]): The types of the institution (e.g., education, funder, healthcare, company, archive, nonprofit, government, facility, other).
    """

    admin: Admin
    domains: List[str]
    established: Optional[int]
    external_ids: List[ExternalId]
    id: HttpUrl
    links: List[Link]
    locations: List[Location]
    names: List[Name]
    relationships: List[Relationship]
    status: str
    types: List[str]

    @property
    def id_without_prefix(self) -> str:
        """
        Returns the ID without the 'https://ror.org/' prefix.

        Returns:
            str: The ID without the prefix.
        """
        if self.id is not None:
            return str(self.id).replace("https://ror.org/", "")
        return ""
