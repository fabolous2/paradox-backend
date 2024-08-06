import datetime
from uuid import UUID
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Feedback:
    id: UUID
    product_id: UUID
    user_id: int
    text: str
    stars: int
    time: datetime.datetime = field(default=datetime.datetime.now(datetime.UTC))
    is_active: bool = field(default=True)
