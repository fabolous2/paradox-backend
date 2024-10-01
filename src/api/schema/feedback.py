from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field


class FeedbackProduct(BaseModel):
    id: UUID


class CreateFeedback(BaseModel):
    product: FeedbackProduct
    stars: Optional[int] = Field(le=5, default=None)
    text: str = Field(max_length=500)
