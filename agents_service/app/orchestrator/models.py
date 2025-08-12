from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, constr, conint


class AgentRequest(BaseModel):
    """
    Generic model representing API request parameters with nested dictionary.
    """

    message: str = Field(..., description="User's message")
