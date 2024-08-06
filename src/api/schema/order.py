from uuid import UUID
from typing import Optional, Union, Any

from pydantic import BaseModel, EmailStr, Field


class BaseOrder(BaseModel):
    login: Optional[Any]
    password: Optional[Any]


class SupercellData(BaseModel):
    email: EmailStr
    code: int = Field(ge=6, le=6)
    

class RobloxData(BaseOrder):
    login: str
    password: int = Field(ge=6, le=6)
    two_factor_code: Optional[int]
    

class CreateOrderDTO(BaseModel):
    user_id: int
    product_id: UUID
    additional_data: Optional[Union[SupercellData, RobloxData, BaseOrder]]
