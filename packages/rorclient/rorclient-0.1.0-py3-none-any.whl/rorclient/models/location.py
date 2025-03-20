"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Pydantic models for locations in the ROR API.
"""

from pydantic import BaseModel


class GeonamesDetails(BaseModel):
    """
    Geographical details of the organization's location.

    Attributes:
        continent_code (str): The continent code of the location.
        continent_name (str): The name of the continent.
        country_code (str): The country code of the location.
        country_name (str): The name of the country.
        country_subdivision_code (str): The subdivision code of the country.
        country_subdivision_name (str): The name of the subdivision.
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.
        name (str): The name of the location.
    """

    continent_code: str
    continent_name: str
    country_code: str
    country_name: str
    country_subdivision_code: str
    country_subdivision_name: str
    lat: float
    lng: float
    name: str


class Location(BaseModel):
    """
    The location of the organization.

    Attributes:
        geonames_details (GeonamesDetails): Geographical details of the location.
        geonames_id (int): The Geonames ID of the location.
    """

    geonames_details: GeonamesDetails
    geonames_id: int
