from .utils.exceptions import ErrorWebhook
from typing import Optional

class FastApiManager:
    def __init__(
                self,
                app_fastapi,
                end_point_invoice: Optional[str]=None,
                end_point_payoff: Optional[str]=None
                ):
        self.__app_fastapi=app_fastapi
        self.__end_point_invoice=end_point_invoice
        self.__end_point_payoff=end_point_payoff

    namewebhook='FastApi'

    def _set_webhook(self,
                    app_crystalpay
                    ) -> None:
        from fastapi import FastAPI, Request, Response
        self.__app_fastapi: FastAPI
        if not isinstance(self.__app_fastapi, FastAPI):
            raise ErrorWebhook('You must use an instance fastapi.FastApi')

        if not self.__end_point_invoice and not self.__end_point_payoff:
            raise ErrorWebhook('You should use at least one end point')

        if self.__end_point_invoice:
            @self.__app_fastapi.post(self.__end_point_invoice)
            async def handler_aiocrystal(request: Request):
                if app_crystalpay.asyncc:
                    await app_crystalpay.updates_feed(await request.json(), typee='invoice')
                else:
                    app_crystalpay.updates_feed(await request.json(), typee='invoice')
                return Response(content="Success", status_code=200)
        if self.__end_point_payoff:
            @self.__app_fastapi.post(self.__end_point_payoff)
            async def handler_aiocrystal(request: Request):
                if app_crystalpay.asyncc:
                    await app_crystalpay.updates_feed(await request.json(), typee='payoff')
                else:
                    app_crystalpay.updates_feed(await request.json(), typee='payoff')
                return Response(content="Success", status_code=200)