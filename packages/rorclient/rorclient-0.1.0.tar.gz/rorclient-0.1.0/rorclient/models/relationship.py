"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for relationships in the ROR API.
"""

from typing import Optional

from pydantic import BaseModel, HttpUrl


class Relationship(BaseModel):
    """
    Related organizations in ROR.

    Attributes:
        label (str): The label of the related organization.
        type (str): The type of the relationship (e.g., related, parent, child, predecessor, successor).
        id (HttpUrl): The ROR ID of the related organization.
    """

    label: str
    type: str
    id: HttpUrl
    record: Optional["Institution"] = None  # type: ignore

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
