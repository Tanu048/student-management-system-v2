from pydantic import BaseModel, Field
from typing import List

class ValidateStudent(BaseModel):
    name: str = Field(..., min_length=1)
    std: str = Field(..., min_length=1)
    roll: str = Field(..., min_length=1)
    marks: List[int] = Field(
        min_length=1, max_length=5
    )  # best done via annotation


class MessageResponse(BaseModel):
    message: str
