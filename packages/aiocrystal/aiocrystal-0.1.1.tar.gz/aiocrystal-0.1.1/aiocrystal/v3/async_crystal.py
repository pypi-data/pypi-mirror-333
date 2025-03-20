from typing import Optional, Callable, List

import requests, aiohttp

from ..utils.types import CallbackInvoice, CallbackPayoff
from ..utils.exceptions import *
from ..utils import signature
from .models import *

class Balance():
    def __init__(
                self,
                request: Callable):
        self.request=request

    async def list(self, hide_empty: Optional[bool]=None) -> BalanceList:
        data: dict=await self.request('/balance/list/', json_add={'hide_empty' : hide_empty})
        return BalanceList(**data)

    async def get(self, method: str) -> BalanceGet:
        return BalanceGet(**await self.request('/balance/get/', json_add={'method' : method}))


class Method():
    def __init__(
                self,
                request: Callable):
        self.request=request
    
    async def list(self, compact: Optional[bool]=None) -> MethodList:
        return MethodList(**await self.request('/method/list/', json_add={'compact' : compact}))

    async def get(self, method: str) -> MethodGet:
        return MethodGet(**await self.request('/method/get/', json_add={'method' : method}))

    async def edit(
                    self, 
                    method: str,
                    enabled: Optional[bool]=None,
                    extra_commission_percent: Optional[int]=None
                   ):
        
        json={
            'method' : method
        }
        if enabled != None:
            json['enabled']=enabled
        if extra_commission_percent != None:
            json['extra_commission_percent']=extra_commission_percent

        await self.request('/method/edit/', json_add=json)

class Invoice():
    def __init__(
                self,
                request: Callable):
        self.request=request

    async def create(self,
                    amount: int | float,
                    lifetime: int=30,
                    type: Literal['purchase', 'topup']='purchase',
                    amount_currency: Optional[str]=None,
                    required_method: Optional[str]=None,
                    description: Optional[str]=None,
                    redirect_url: Optional[str]=None,
                    callback_url: Optional[str]=None,
                    extra: Optional[str]=None,
                    payer_details: Optional[str]=None
                    ) -> InvoiceCreate:

        json=dict(locals())
        del json['self']
        return InvoiceCreate(**await self.request('/invoice/create/', json_add=json))

    async def info(self, id: str) -> InvoiceInfo:
        return InvoiceInfo(**await self.request('/invoice/info/', json_add={'id' : id}))

class Payoff():
    def __init__(
                self,
                request: Callable,
                salt: str
                ):
        self.request=request
        self.__salt=salt

    async def create(
            self,
            method: str,
            wallet: str,
            amount: int | float,
            subtract_from: Literal['amount', 'balance'],
            amount_currency: Optional[str]=None,
            wallet_extra: Optional[str]=None,
            extra: Optional[str]=None,
            callback_url: Optional[str]=None
                ) -> PayoffCreate:
        json=dict(locals())
        del json['self']
        json['signature']=await signature.generete_signature_valider_async(salt=self.__salt, 
                                                                           amount=amount,
                                                                           method=method,
                                                                           wallet=wallet
                                                                           )
        return PayoffCreate(**self.request('/payoff/create/', json_add=json))

    async def submit(self, id) -> PayoffInfo:
        json={
            'id' : id,
            'signature' : await signature.generete_signature_valider_async(salt=self.__salt, id=id)
        }
        return PayoffInfo(**self.request('/payoff/submit/', json_add=json))

    async def cancel(self, id) -> PayoffInfo:
        json={
            'id' : id,
            'signature' : await signature.generete_signature_valider_async(salt=self.__salt, id=id)
        }
        return PayoffInfo(**self.request('/payoff/cancel/', json_add=json))

    async def info(self, id) -> PayoffInfo:
        return PayoffInfo(**self.request('/payoff/info/', json_add={'id' : id}))

class Swap():
    class Pair():
        def __init__(
                    self,
                    request: Callable
                    ):
            self.request=request
            
        async def list(
                    self, 
                    page: int, 
                    items: int, 
                    source: Optional[str]=None, 
                    target: Optional[str]=None) -> SwapPairList:
            json=dict(locals())
            del json['self']
            return SwapPairList(**await self.request('/swap/pair/list/', json_add=json))
        
        async def get(self, pair_id: int) -> SwapPairGet:
            return SwapPairGet(**await self.request('/swap/pair/get/', json_add={'pair_id' : pair_id}))

    def __init__(
                self,
                request: Callable,
                salt: str
                ):
        self.request=request
        self.__salt=salt
        self.pair=self.Pair(request)

    async def create(
                    self, 
                    pair_id,
                    amount,
                    amount_type
                    ) -> SwapCreate:
        json=dict(locals())
        del json['self']
        json['signature']=await signature.generete_signature_valider_async(salt=self.__salt, amount=amount, pair_id=pair_id)
        return SwapCreate(**self.request('/swap/create/', json_add=json))

    async def submit(self, id) -> SwapInfo:
        json={
            'id' : id,
            'signature' : await signature.generete_signature_valider_async(salt=self.__salt, id=id)
        }
        return SwapInfo(**await self.request('/swap/submit/', json_add=json))
    
    async def cancel(self, id):
        json={
            'id' : id,
            'signature' : await signature.generete_signature_valider_async(salt=self.__salt, id=id)
        }
        return SwapInfo(**await self.request('/swap/cancel/', json_add=json))
    
    async def info(self, id):
        return SwapInfo(**await self.request('/swap/info/', json_add={'id' : id}))

class Transfer():
    def __init__(
                self,
                request: Callable,
                salt: str
                ):
        self.request=request
        self.__salt=salt
    
    async def create(
                self,
                method: str,
                amount: int | float,
                receiver: str,
                description: Optional[str]=None
                ) -> TransferCreate:
        json=dict(locals())
        del json['self']
        json['signature']=await signature.generete_signature_valider_async(salt=self.__salt, amount=amount, method=method, receiver=receiver)
        return TransferCreate(**self.request('/t    ransfer/create/', json_add=json))

    async def submit(self, id) -> TransferInfo:
        json={
            'id' : id,
            'signature' : await signature.generete_signature_valider_async(salt=self.__salt, id=id)
        }
        return TransferCreate(**self.request('/transfer/submit/', json_add=json))
    
    async def info(self, id) -> TransferInfo:
        return TransferCreate(**self.request('/transfer/submit/', json_add={'id' : id}))

class Ticker():
    def __init__(
                self,
                request: Callable
                ):
        self.request=request
    
    async def list(self) -> List:
        return (await self.request('/ticker/list/'))['tickers']

    async def get(  
                self,
                tickers: List,
                base_currency: Optional[str]='RUB'
                  ) -> TickerGet:
        json={
            'tickers' : tickers,
            'base_currency' : base_currency
        }

        return TickerGet(**await self.request('/ticker/get/', json_add=json))

class Report():
    class Invoice():
        def __init__(
                self,
                request: Callable
                ):
            self.request=request

        async def history(
                self, 
                page: int,
                items: int,
                period: int,
                export_csv: Optional[bool]=None
                ) -> ReportInvoiceHistory | str:
            json=dict(locals())
            del json['self']
            if export_csv:
                return await self.request('/report/invoice/history/', json_add=json)
            return ReportInvoiceHistory(**await self.request('/report/invoice/history/', json_add=json))

        async def summary(
                self,
                period: int
                ) -> ReportSummary:

            return ReportSummary(**await self.request('/report/invoice/summary/', json_add={'period' : period}))

    class Payoff():
        def __init__(
                self,
                request: Callable
                ):
            self.request=request
        
        async def history(
                self, 
                page: int,
                items: int,
                period: int,
                export_csv: Optional[bool]=None
                ) -> ReportPayoffHistory | str:
            json=dict(locals())
            del json['self']
            if export_csv:
                return await self.request('/report/payoff/history/', json_add=json)
            return ReportPayoffHistory(**await self.request('/report/payoff/history/', json_add=json))

        async def summary(
                self,
                period: int
                ) -> ReportSummary:
            return ReportSummary(**await self.request('/report/payoff/summary/', json_add={'period' : period}))

    class Swap():
        def __init__(
                self,
                request: Callable
                ):
            self.request=request

        async def history(
                self, 
                page: int,
                items: int,
                period: int,
                export_csv: Optional[bool]=None
                ) -> ReportSwapHistory | str:
            json=dict(locals())
            del json['self']
            if export_csv:
                return await self.request('/report/swap/history/', json_add=json)
            return ReportSwapHistory(**await self.request('/report/swap/history/', json_add=json))

    class Transfer():
        def __init__(
                self,
                request: Callable
                ):
            self.request=request
        
        async def history(
                self, 
                page: int,
                items: int,
                period: int,
                export_csv: Optional[bool]=None
                ) -> ReportTransferHistory | str:
            json=dict(locals())
            del json['self']
            if export_csv:
                return await self.request('/report/transfer/history/', json_add=json)
            return ReportTransferHistory(**await self.request('/report/transfer/history/', json_add=json))
    def __init__(
                self,
                request: Callable
                ):
        self.invoice=self.Invoice(request)
        self.payoff=self.Payoff(request)
        self.swap=self.Swap(request)
        self.transfer=self.Transfer(request)

class CrystalPay(Balance):
    def __init__(self,
                auth_login: str, 
                auth_secret: str, 
                salt: str, 
                webhook_manager: Optional[Callable]=None,
                check_auth: bool=True):
        self.__auth_login=auth_login
        self.__auth_secret=auth_secret
        self.__salt=salt
        self.base_url='https://api.crystalpay.io/v3'
        if check_auth:
            result = requests.post(
                f"{self.base_url}/method/list/", 
                json = {'auth_login': self.__auth_login, 'auth_secret': self.__auth_secret}, 
                headers = {'Content-Type': 'application/json'} 
            ).json()
            if result['error']:
                raise(InvalidAuth(', '.join(result['errors'])))
        self.__isset_webhook=False
        if webhook_manager:
            webhook_manager._set_webhook(self)
            self.__isset_webhook=True

        self.asyncc=True
        self.invoice_handlers=list()
        self.payoff_handlers=list()
        self.balance=Balance(self.request)
        self.method=Method(self.request)
        self.invoice=Invoice(self.request)
        self.payoff=Payoff(self.request, salt=self.__salt)
        self.swap=Swap(self.request, salt=self.__salt)
        self.ticker=Ticker(self.request)
        self.report=Report(self.request)

    async def request(self,
                    method: str,
                    json_add: Optional[dict]=None
                    ):
        async with aiohttp.ClientSession() as session:
            json={
                'auth_login' : self.__auth_login,
                'auth_secret': self.__auth_secret
            }
            if json_add:
                for i in json_add.keys():
                    json[i]=json_add[i]
            async with session.post(f'{self.base_url}/{method}', json=json) as resp:
                try:
                    result=await resp.json()
                except:
                    return await resp.text()
                if result['error']:
                    raise(RequestCrystalPayError(', '.join(result['errors'])))
                del result['error']
                del result['errors']
                return result
            
    async def get_me(self) -> GetMe:
        return GetMe(**await self.request('/me/info/'))
    
    def callback_payoff(self, *args):
        '''
        :Args:
        *args: this filter
        '''
        if not self.__isset_webhook:
            raise ErrorWebhook('Webhook is not set')
        filters=list()
        for i in args:
            filters.append(i)
        def decorator(f):
            self.payoff_handlers.append({'func': f, 'filter': filters})
            return f
        return decorator

    def callback_invoice(self, *args):
        '''
        :Args:
        *args: this filter
        '''
        if not self.__isset_webhook:
            raise ErrorWebhook('Webhook is not set')
        filters=list()
        for i in args:
            filters.append(i)
        def decorator(f):
            self.invoice_handlers.append({'func': f, 'filter': filters})
            return f
        return decorator
    
    async def updates_feed(self, json_data: dict, typee: Literal['invoice', 'payoff']):
        if not await signature.signature_valider_async(salt=self.__salt, id=json_data['id'], signature=json_data['signature']):
            return
        del json_data['signature']
        if typee == 'invoice':
            handlers=self.invoice_handlers
        elif typee == 'payoff':
            handlers=self.payoff_handlers
        else:
            return
        for i in handlers:
            isfilter=True
            for t in i['filter']:
                try:
                    isfilter=await t((CallbackInvoice if typee == 'invoice' else CallbackPayoff)(**json_data))
                except:
                    isfilter=t((CallbackInvoice if typee == 'invoice' else CallbackPayoff)(**json_data))
            if isfilter:
                try:
                    await i['func']((CallbackInvoice if typee == 'invoice' else CallbackPayoff)(**json_data))
                except:
                    i['func']((CallbackInvoice if typee == 'invoice' else CallbackPayoff)(**json_data))