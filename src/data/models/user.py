from typing import Optional

from sqlalchemy import Integer, DECIMAL, JSON, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base


class UserModel(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(Numeric, primary_key=True)
    referral_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    balance: Mapped[Optional[float]] = mapped_column(DECIMAL, nullable=False, default=0)
    used_coupons: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    referral_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    transactions = relationship('TransactionModel', back_populates='user')
    orders = relationship('OrderModel', back_populates='user')
    feedbacks = relationship('FeedbackModel', back_populates='user')
