import datetime
from uuid import UUID
from enum import Enum
from dataclasses import dataclass, field
from typing import Mapping, Any


class TransactionType(Enum):
    DEBIT = 'DEBIT'
    DEPOSIT = 'DEPOSIT'


class TransactionCause(Enum):
    DONATE = 'DONATE'
    ADMIN_DEPOSIT = 'ADMIN_DEPOSIT'
    ADMIN_DEBIT = 'ADMIN_DEBIT'
    COUPON = 'COUPON'
    REFUND = 'REFUND'
    PAYMENT = 'PAYMENT'
    REFERRAL = 'REFERRAL'


@dataclass(frozen=True)
class Transaction:
    id: UUID
    user_id: int
    type: TransactionType
    cause: TransactionCause
    amount: float
    is_successful: bool = field(default=False)
    time: datetime.datetime = field(default=datetime.datetime.now(datetime.UTC))
    payment_data: Mapping[str, Any] = field(default=None)
