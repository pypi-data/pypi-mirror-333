# src/stratio/api/config/clusters_config.py
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class LambdasConfig(BaseModel):
    marketplace_subscribers_prefix: str
    start_stop_stratio_cluster_prefix: str
    start_stratio_applications_prefix: str
    remove_stratio_cluster_prefix: str


class KeosConfig(BaseModel):
    workspaces_local_folder: str
    base_image: str
    vault_key: str
    vault_key_env_var: str


class ClustersConfig(BaseModel):
    # DynamoDB table filter regex
    table_filter_regex: str = Field(
        "^MarketplaceSubscribers.*$", description="Regex pattern to filter DynamoDB tables for customers."
    )
    # Workspaces bucket filter regex
    workspaces_bucket_regex: str = Field(
        ".*-automations-stratio-artifacts$", description="Regex pattern to filter workspaces."
    )

    # Lambdas config
    lambdas: Optional[LambdasConfig] = None

    # KEOS config
    keos: Optional[KeosConfig] = None

    @field_validator("table_filter_regex", mode="before")
    def validate_regex(cls, v):
        try:
            re.compile(v)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern for table_filter_regex: {e}") from e
        return v
