# src/stratio/api/config/universe_config.py

from pydantic import BaseModel, Field


class UniverseConfig(BaseModel):
    _not_a_placeholder = "^(?!.*<replace>).*$"

    region: str = Field("eu-west-1", description="ECR preferred region.")
    customers_ou_name: str = Field("Customers", description="Name of the Customers OU.")

    # TODO: Uncomment when required to validate placeholders
    # @field_validator("organization_id", "root_ou_id", "customers_ou_id", mode="before")
    # def validate_regex(cls, v):
    #     try:
    #         re.compile(v)
    #         if not re.match(cls._not_a_placeholder.default, v):
    #             raise ValueError(f"Replace the placeholders for actual environment values: {cls._not_a_placeholder}")
    #     except re.error as e:
    #         raise ValueError(f"Invalid regex pattern for table_filter_regex: {e}") from e
    #     return v
