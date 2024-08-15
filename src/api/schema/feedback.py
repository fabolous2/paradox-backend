from uuid import UUID

from pydantic import BaseModel, Field


class FeedbackProduct(BaseModel):
    id: UUID


class CreateFeedback(BaseModel):
    product: FeedbackProduct
    stars: int = Field(le=5)
    text: str = Field(le=500)

