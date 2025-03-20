"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Configuration class for the RORClient package.
"""

from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class Config(BaseModel):
    base_url: HttpUrl = Field(
        default=HttpUrl("https://api.ror.org/v2/"),
        description="Base URL for the ROR API",
    )
    max_retry_time: PositiveInt = Field(
        default=60, description="Maximum retry time in seconds"
    )
    max_retries: PositiveInt = Field(default=5, description="Maximum number of retries")


config = Config()
