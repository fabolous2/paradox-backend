import datetime
from uuid import UUID
from enum import Enum
from dataclasses import dataclass, field


class TransactionType(Enum):
    DEBIT = 'Списание'
    DEPOSIT = 'Пополнение'


class TransactionCause(Enum):
    DONATE = 'Донат'
    ADMIN_REPLENISHMENT = 'Пополнение администратором'
    COUPON = 'Ввод промокода'
    REFUND = 'Возврат'
    PAYMENT = 'Оплата заказа'
    REFERRAL = 'Реферальный бонус'


@dataclass(frozen=True)
class Transaction:
    id: UUID
    user_id: int
    type: TransactionType
    cause: TransactionCause
    amount: float
    time: datetime.datetime = field(default=datetime.datetime.now(datetime.UTC))
    