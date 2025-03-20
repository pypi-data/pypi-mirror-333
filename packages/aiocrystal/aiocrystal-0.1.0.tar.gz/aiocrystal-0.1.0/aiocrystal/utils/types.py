from typing import Literal, Optional
from pydantic import BaseModel
from enum import Enum

class InvoiceType(Enum):
    purchase='purchase'
    topup='topup'

class InvoiceState(Enum):
    notpayed='notpayed'
    processing='processing'
    wrongamount='wrongamount'
    failed='failed'
    payed='payed'

class PayoffState(Enum):
    created='created'
    processing='processing'
    failed='failed'
    payed='payed'
    canceled='canceled'

class SwapState(Enum):
    created='created'
    processing='processing'
    failed='failed'
    success='success'
    canceled='canceled'

class SwapAmountType(Enum):
    source='source'
    target='target'

class TransferState(Enum):
    created='created'
    processing='processing'
    failed='failed'
    success='success'
    canceled='canceled'

class TransferType(Enum):
    internal='internal'
    system='system'

class CallbackInvoice(BaseModel):
    id: str
    url: str
    state: Literal['notpayed', 'processing', 'wrongamount', 'failed', 'payed']
    type: Literal['purchase', 'topup']
    method: str
    required_method: Optional[str]
    amount_currency: str
    rub_amount: int | float
    initial_amount: int | float
    remaining_amount: int | float
    balance_amount: int | float
    commission_amount: int | float
    description: Optional[str]
    redirect_url: Optional[str]
    callback_url: str
    extra: Optional[str]
    created_at: str
    expired_at: str
    final_at: str

class CallbackPayoff(BaseModel):
    id: str
    state: Literal['created', 'processing', 'failed', 'payed', 'canceled']
    subtract_from: Literal['amount', 'balance']
    method: str
    amount_currency: str
    amount: int | float
    rub_amount: int | float
    receive_amount: int | float
    deduction_amount: int | float
    commission_amount: int | float
    wallet: str
    message: Optional[str]
    callback_url: str
    extra: Optional[str]
    created_at: str
    final_at: str


CallbackPayoff(**{
    "signature": "9eabbecc21c8bc968b73291bb19def2a10c8251c",
    "id": "123456789_dpWminAiaqwTcBOJVlFk",
    "state": "payed",
    "subtract_from": "balance",
    "method": "ETHEREUM",
    "amount_currency": "ETH",
    "amount": "0.0005",
    "rub_amount": "151",
    "receive_amount": "0.0005",
    "deduction_amount": "0.002",
    "commission_amount": "0.0015",
    "wallet": "examplewallet",
    "message": None,
    "callback_url": "https://example.com/handler",
    "extra": None,
    "created_at": "2024-01-01 11:11:11",
    "final_at": "2024-01-01 11:11:11"
})