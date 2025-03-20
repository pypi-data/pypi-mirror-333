"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for administrative information in the ROR API.
"""

from datetime import date

from pydantic import BaseModel


class AdminCreated(BaseModel):
    """
    Metadata about the creation of the record.

    Attributes:
        date (date): The date the record was created.
        schema_version (str): The schema version used when the record was created.
    """

    date: date
    schema_version: str


class AdminLastModified(BaseModel):
    """
    Metadata about the last modification of the record.

    Attributes:
        date (date): The date the record was last modified.
        schema_version (str): The schema version used when the record was last modified.
    """

    date: date
    schema_version: str


class Admin(BaseModel):
    """
    Container for administrative information about the record.

    Attributes:
        created (AdminCreated): Metadata about the creation of the record.
        last_modified (AdminLastModified): Metadata about the last modification of the record.
    """

    created: AdminCreated
    last_modified: AdminLastModified
