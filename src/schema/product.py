from uuid import UUID
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Product:
    id: UUID
    name: str
    description: str
    price: float
    instruction: str = field(default=None)
    purchase_count: int = field(default=0)
