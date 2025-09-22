"""Schema definitions for API data validation and serialization."""
from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Defines how an error message is displayed """
    message: str
