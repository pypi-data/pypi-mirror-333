"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for search in the ROR API.
"""

from typing import List

from institution import Institution
from pydantic import BaseModel


class Container(BaseModel):
    """
    Represents a container of metadata information such as types, countries, continents, or statuses.

    Attributes:
        id (str): The unique identifier for the container.
        title (str): The title or name associated with the container.
        count (int): The number of items in this category.
    """

    id: str
    title: str
    count: int


class Meta(BaseModel):
    """
    Encapsulates metadata information about the search results, including types, countries, continents, and statuses.

    Attributes:
        types (List[Container]): A list of containers representing different types.
        countries (List[Container]): A list of containers representing different countries.
        continents (List[Container]): A list of containers representing different continents.
        statuses (List[Container]): A list of containers representing different statuses.
    """

    types: List[Container]
    countries: List[Container]
    continents: List[Container]
    statuses: List[Container]


class SearchResult(BaseModel):
    """
    Represents the result of a search query to the ROR API, including metadata and a list of institutions.

    Attributes:
        number_of_results (int): The total number of results found for the search query.
        time_taken (int): The time taken to perform the search query in milliseconds.
        items (List[Institution]): A list of Institution objects representing the search results.
    """

    number_of_results: int
    time_taken: int
    items: List[Institution]
