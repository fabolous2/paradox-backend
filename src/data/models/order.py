import enum
import uuid
import datetime
from typing import Mapping, Any

from sqlalchemy import Enum, UUID, TIMESTAMP, String, Integer, DECIMAL, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base
from src.schema.order import OrderStatus


class OrderModel(Base):
    __tablename__ = "order"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('product.id'))
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[enum.Enum] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PROGRESS)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    time: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.datetime.now(datetime.UTC),
    )
    additional_data: Mapped[Mapping[str, Any]] = mapped_column(JSON, nullable=True)

    user = relationship('UserModel', back_populates='orders')
    product = relationship('ProductModel', back_populates='orders')
