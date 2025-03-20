"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for links in the ROR API.
"""

from pydantic import BaseModel, HttpUrl


class Link(BaseModel):
    """
    The organization's website and Wikipedia page.

    Attributes:
        type (str): The type of the link (e.g., website, wikipedia).
        value (HttpUrl): The URL of the link.
    """

    type: str
    value: HttpUrl
