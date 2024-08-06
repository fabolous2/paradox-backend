from uuid import UUID

from pydantic import BaseModel, Field


class FeedbackProduct(BaseModel):
    id: UUID


class FeedbackUser(BaseModel):
    id: int


class CreateFeedback(BaseModel):
    user: FeedbackUser
    product: FeedbackProduct
    stars: int = Field(le=5)
    text: str = Field(le=500)

