from typing import Literal, Optional
from pydantic import BaseModel

class InvoiceType():
    purchase='purchase'
    topup='topup'

class InvoiceState():
    notpayed='notpayed'
    processing='processing'
    wrongamount='wrongamount'
    failed='failed'
    payed='payed'

class PayoffState():
    created='created'
    processing='processing'
    failed='failed'
    payed='payed'
    canceled='canceled'

class SwapState():
    created='created'
    processing='processing'
    failed='failed'
    success='success'
    canceled='canceled'

class SwapAmountType():
    source='source'
    target='target'

class TransferState():
    created='created'
    processing='processing'
    failed='failed'
    success='success'
    canceled='canceled'

class TransferType():
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


