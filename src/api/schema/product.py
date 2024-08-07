import uuid
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateProduct(BaseModel):
    id: uuid.UUID = Field(default=uuid.uuid4())
    name: str
    description: str
    price: Decimal
    instruction: Optional[str] = Field(default=None)
    purchase_count: Optional[int] = Field(default=0)
