import uuid
from typing import Optional

from sqlalchemy import UUID, String, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    instruction: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    purchase_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    game: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)

    orders = relationship('OrderModel', back_populates='product')
    feedbacks = relationship('FeedbackModel', back_populates='product')
    