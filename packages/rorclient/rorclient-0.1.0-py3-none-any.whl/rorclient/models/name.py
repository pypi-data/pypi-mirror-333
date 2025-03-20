"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for names in the ROR API.
"""

from typing import List, Optional

from pydantic import BaseModel


class Name(BaseModel):
    """
    Names the organization goes by.

    Attributes:
        lang (Optional[str]): The language of the name, if any.
        types (List[str]): The types of the name (e.g., acronym, alias, label, ror_display).
        value (str): The name value.
    """

    lang: Optional[str]
    types: List[str]
    value: str
