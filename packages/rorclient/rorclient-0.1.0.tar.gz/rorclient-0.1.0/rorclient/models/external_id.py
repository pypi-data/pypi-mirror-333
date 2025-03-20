"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for external IDs in the ROR API.
"""

from typing import List, Optional

from pydantic import BaseModel


class ExternalId(BaseModel):
    """
    Other identifiers for the organization.

    Attributes:
        all (List[str]): A list of all external IDs.
        preferred (Optional[str]): The preferred external ID, if any.
        type (str): The type of the external ID (e.g., fundref, grid, isni, wikidata).
    """

    all: List[str]
    preferred: Optional[str]
    type: str
