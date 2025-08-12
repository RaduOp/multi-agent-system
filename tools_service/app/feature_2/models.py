from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, constr, conint
from datetime import datetime


# Request models
class NestedOptions(BaseModel):
    """
    Nested options dictionary with flexible keys and values.
    """

    options: Dict[str, Any] = Field(
        default_factory=dict, description="A dictionary of optional settings or flags"
    )


class FeatureRequest(BaseModel):
    """
    Generic model representing API request parameters with nested dictionary.
    """

    resource_id: constr(min_length=1, max_length=50) = Field(
        ..., description="Identifier of the resource"
    )
    limit: conint(ge=1, le=100) = Field(
        10, description="Maximum number of items to process or return"
    )
    offset: conint(ge=0) = Field(
        0,
        description="Number of items to skip before starting to collect the result set",
    )
    include_metadata: Optional[bool] = Field(
        False, description="Flag to include additional metadata"
    )
    timeout_seconds: Optional[conint(ge=1, le=120)] = Field(
        30, description="Timeout in seconds for the request"
    )
    user_token: Optional[constr(min_length=10, max_length=100)] = Field(
        None, description="Authentication token for the user"
    )
    nested_options: Optional[NestedOptions] = Field(
        None, description="Nested dictionary with additional options"
    )


# Response models
class ResultItem(BaseModel):
    # Define the fields each item in the results list has
    # For example:
    id: int
    name: str
    value: float


class DataPayload(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the results")
    results: List[ResultItem] = Field(..., description="List of result items")


class FeatureResponse(BaseModel):
    status: str = Field(..., description="Result status, e.g., 'success' or 'error'")
    data: DataPayload = Field(..., description="The actual data payload")
