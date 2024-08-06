from enum import Enum
from decimal import Decimal

from pydantic import BaseModel, Field


class RawSumma(BaseModel):
    amount: Decimal = Field(ge=10, le=50000)


class TopUpMethod(Enum):
    SBP = 'sbp'
    CARD = 'card'
    