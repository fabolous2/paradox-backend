import datetime
from enum import Enum
from uuid import UUID
from dataclasses import dataclass, field
from typing import Mapping, Any


class OrderStatus(Enum):
    PAID = 'Оплачен'
    CLOSED = 'Закрыт'
    COMPLETED = 'Завершен'
    PROGRESS = 'На обработке'


@dataclass(frozen=True)
class Order:
    id: UUID
    user_id: int
    product_id: UUID
    price: float
    name: str
    additional_data: Mapping[str, Any]
    status: OrderStatus = field(default=OrderStatus.PROGRESS)
    time: datetime.datetime = field(default=datetime.datetime.now(datetime.UTC))
