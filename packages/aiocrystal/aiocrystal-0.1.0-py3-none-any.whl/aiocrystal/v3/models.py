from pydantic import BaseModel, Field
from typing import Dict, Literal, Optional, List

class GetMe(BaseModel):
    id: int
    name: str
    status_level: int
    created_at: str

class BalanceList(BaseModel):
    class CurrencyData(BaseModel):
        name: str
        amount: int | float
        currency: str
        amount_accuracy: int | float
    items: Dict[str, CurrencyData]

class BalanceGet(BaseModel):
    method: str
    name: str
    amount: int | float
    currency: str
    amount_accuracy: int |float

class MethodList(BaseModel):

    class SettingsExtraCommissions(BaseModel):
        amount: int | float
        percent: int | float

    class MethodData(BaseModel):
        class SettingsIn(BaseModel):
            enabled: bool
            extra_commissions: 'MethodList.SettingsExtraCommissions'  # Строковая аннотация

        class SettingsOut(BaseModel):
            enabled: bool
            extra_commissions: 'MethodList.SettingsExtraCommissions'  # Строковая аннотация

        class Settings(BaseModel):
            in_: 'MethodList.MethodData.SettingsIn' = Field(alias="in")  # Строковая аннотация
            out: 'MethodList.MethodData.SettingsOut'  # Строковая аннотация

        name: str
        currency: str
        amount_accuracy: int | float
        minimal_status_level: int
        settings: 'MethodList.MethodData.Settings'  # Строковая аннотация

    items: Dict[str, MethodData]

class MethodGet(BaseModel):
    class SettingsExtraCommissions(BaseModel):
        amount: int | float
        percent: int | float

    class MethodData(BaseModel):
        class SettingsIn(BaseModel):
            enabled: bool
            extra_commissions: 'MethodGet.SettingsExtraCommissions'  # Строковая аннотация

        class SettingsOut(BaseModel):
            enabled: bool
            extra_commissions: 'MethodGet.SettingsExtraCommissions'  # Строковая аннотация

        class Settings(BaseModel):
            in_: 'MethodGet.MethodData.SettingsIn' = Field(alias="in")  # Строковая аннотация
            out: 'MethodGet.MethodData.SettingsOut'  # Строковая аннотация

    name: str
    currency: str
    amount_accuracy: int | float
    minimal_status_level: int
    settings: 'MethodGet.MethodData.Settings'  # Строковая аннотация

class InvoiceCreate(BaseModel):
    id: str
    url: str
    type: Literal['purchase', 'topup']
    rub_amount: int | float

class InvoiceInfo(BaseModel):
    id: str
    url: str
    state: Literal['notpayed', 'processing', 'wrongamount', 'failed', 'payed']
    type: Literal['purchase', 'topup']
    method: Optional[str]
    required_method: Optional[str]
    amount_currency: str
    rub_amount: int | float
    initial_amount: int | float
    remaining_amount: int | float
    balance_amount: int | float
    commission_amount: int | float
    description: Optional[str]
    redirect_url: Optional[str]
    callback_url: Optional[str]
    extra: Optional[str]
    created_at: str
    expired_at: str
    final_at: Optional[str]

class PayoffCreate(BaseModel):
    id: str
    subtract_from: Literal['amount', 'balance']
    method: str
    amount_currency: str
    amount: int | float
    rub_amount: int | float
    receive_amount: int | float
    deduction_amount: int| float
    commission_amount: int | float
    wallet: str

class PayoffInfo(BaseModel):
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
    callback_url: Optional[str]
    extra: Optional[str]
    created_at: str
    final_at: Optional[str]

class SwapPairList(BaseModel):
    class PairData(BaseModel):
        method: str
        name: str
        currency: str

    class Pair(BaseModel):
        source: 'SwapPairList.PairData'
        target: 'SwapPairList.PairData'
        price: int | float

    items: Dict[str, Pair]
    has_next_page: bool

class SwapPairGet(BaseModel):
    class PairData(BaseModel):
        method: str
        name: str
        currency: str

    source: 'SwapPairList.PairData'
    target: 'SwapPairList.PairData'
    price: int | float


class SwapCreate(BaseModel):
    class SwapCreateData(BaseModel):
        method: str
        currency: str
        amount: int | float
    id: str
    pair_id: int
    amount_type: Literal['source', 'target']
    amount: int | float
    price: int | float
    source: 'SwapCreate.SwapCreateData'
    target: 'SwapCreate.SwapCreateData'

class SwapInfo(BaseModel):
    class SwapCreateData(BaseModel):
        method: str
        currency: str
        amount: int | float

    id: str
    state: Literal['created', 'processing', 'failed', 'success', 'canceled']
    pair_id: int
    amount_type: Literal['source', 'target']
    amount: int | float
    price: int | float
    created_at: str
    expired_at: str
    final_at: str

    source: 'SwapInfo.SwapCreateData'
    target: 'SwapInfo.SwapCreateData'

class TransferCreate(BaseModel):
    id: int
    method: str
    amount_currency: str
    amount: int | float
    sender: str
    receiver: str

class TransferInfo(BaseModel):
    id: int
    state: Literal['created', 'processing', 'failed', 'success', 'canceled']
    type: Literal['internal', 'system']
    method: str
    amount_currency: str
    amount: int | float
    sender: str
    receiver: str
    description: Optional[str]
    created_at: str
    final_at: str

class TickerGet(BaseModel):
    class Currency(BaseModel):
        price: int | float
    base_currency: str
    currencies: Dict[str, Currency]

class ReportSummary(BaseModel):
    payed_rub_amount: int | float
    payed_count: int
    total_count: int
    conversion_percent: int

class ReportInvoiceHistory(BaseModel):
    items: List['InvoiceInfo']
    has_next_page: bool

class ReportPayoffHistory(BaseModel):
    items: List['PayoffInfo']
    has_next_page: bool

class ReportSwapHistory(BaseModel):
    items: List['SwapInfo']
    has_next_page: bool

class ReportTransferHistory(BaseModel):
    items: List['TransferInfo']
    has_next_page: bool


