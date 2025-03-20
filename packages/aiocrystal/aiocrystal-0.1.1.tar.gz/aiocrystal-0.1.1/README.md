![]('image/aiocrystal_logo.png')


Библиотека полностью повтраяет структуру вложоности https://docs.crystalpay.io/

Создания счета & проверка(не рекомендуеться иза лимита)
``` python
from aiocrystal import CrystalPay
from aiocrystal.utils.types import InvoiceState
import asyncio

cp=CrystalPay(auth_login='name',
              auth_secret='Secret',
              salt='salt'
              )

async def main():
    invoice=await cp.invoice.create(amount=100, description='aiocrystal<3')
    invoice_id=invoice.id
    print(invoice.url)
    while True:
        invoice_state=(await cp.invoice.info(invoice_id)).state
        if InvoiceState.payed == invoice_state:
            print('Succes')
            break
        await asyncio.sleep(5)


asyncio.run(main())
```

WebHook Fastapi & пример фильтров
``` python
from typing import Union

from fastapi import FastAPI

from aiocrystal.v3.async_crystal import CrystalPay
from aiocrystal.utils.types import CallbackInvoice, InvoiceState
from aiocrystal.webhook import FastApiManager

import uvicorn
import asyncio

host=''

app = FastAPI()

cp=CrystalPay(auth_login='name',
     auth_secret='Secret',
     salt='Salt',
     webhook_manager=FastApiManager(
        app_fastapi=app,
        end_point_invoice='/pay/crystalpay'
     )
     )
# пример фильтрации
async def IsPayed(invoice: CallbackInvoice): 
    return invoice.rub_amount >= 100 

async def AntiUnavailableIsPayed(invoice: CallbackInvoice):
    return invoice.state == InvoiceState.payed

@cp.callback_invoice(IsPayed, AntiUnavailableIsPayed) #<- вохможность добавлять несколько фильтров
async def pay_cp(invoice: CallbackInvoice):
    print(f'Пришло: {invoice.rub_amount}')

async def main():
    invoice=await cp.invoice.create(100, callback_url=f'{host}/pay/crystalpay')
    print(invoice.url)


asyncio.run(main())

uvicorn.run(app, host="localhost", port=5000)

