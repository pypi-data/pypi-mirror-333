# src/stratio/api/config/customer_config.py

import re

from pydantic import BaseModel, Field, field_validator


class CustomersConfig(BaseModel):
    # DynamoDB table filter regex
    table_filter_regex: str = Field(
        "^MarketplaceSubscribers.*$", description="Regex pattern to filter DynamoDB tables for customers."
    )

    @field_validator("table_filter_regex", mode="before")
    def validate_regex(cls, v):
        try:
            re.compile(v)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern for table_filter_regex: {e}") from e
        return v
