from nexo.base_client import BaseClient
from typing import Dict, Optional, List, Tuple

from operator import itemgetter
import aiohttp
import asyncio
import json
import time

from nexo.exceptions import NexoAPIException, NEXO_API_ERROR_CODES, NexoRequestException
from nexo.helpers import check_pair_validity, compact_json_dict
from nexo.response_serializers import (
    Balances,
    AdvancedOrderResponse,
    OrderDetails,
    OrderResponse,
    Orders,
    Pairs,
    Transaction,
    Quote,
    TradeHistory,
)


class AsyncClient(BaseClient):
    def __init__(self, api_key, api_secret, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        super().__init__(api_key, api_secret)
        self._init_session()

    @classmethod
    async def create(cls, api_key=None, api_secret=None, loop=None):
        return cls(api_key, api_secret, loop)

    def _init_session(self):
        session = aiohttp.ClientSession(loop=self.loop)
        headers = {
            "Accept": "application/json",
            "User-Agent": "python-nexo",
            "Content-Type": "application/json",
            "X-API-KEY": self.API_KEY,
        }
        session.headers.update(headers)

        self.session = session

    async def close_connection(self):
        if self.session:
            assert self.session
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse):
        json_response = {}

        try:
            json_response = await response.json()
        except Exception:
            if not response.ok:
                raise NexoRequestException(
                    f"Failed to get API response: \nCode: {response.status_code}\nRequest: {str(response.request.body)}"
                )

        try:
            if "errorCode" in json_response:
                if json_response["errorCode"] in NEXO_API_ERROR_CODES:
                    raise NexoAPIException(
                        json_response["errorCode"], await response.text()
                    )
                else:
                    raise NexoRequestException(
                        f'Invalid Response: status: {json_response["errorCode"]}, message: {json_response["errorMessage"]}\n body: {response.request.body}'
                    )
            else:
                if not response.ok:
                    raise NexoRequestException(
                        f"Failed to get API response: \nCode: {response.status_code}\nRequest: {str(response.request.body)}"
                    )

                return json_response

        except ValueError:
            raise NexoRequestException("Invalid Response: %s" % json_response)

    async def _request(
        self, method, path: str, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        # set default requests timeout
        kwargs["timeout"] = 10

        kwargs["data"] = kwargs.get("data", {})
        kwargs["headers"] = kwargs.get("headers", {})

        full_path = self._create_path(path, version)
        uri = self._create_api_uri(full_path)

        nonce = str(int(time.time() * 1000))
        kwargs["headers"]["X-NONCE"] = nonce
        kwargs["headers"]["X-SIGNATURE"] = self._generate_signature(nonce).decode(
            "utf8"
        )

        if kwargs["data"] and method == "get":
            kwargs["params"] = kwargs["data"]
            del kwargs["data"]

        if method != "get" and kwargs["data"]:
            kwargs["data"] = compact_json_dict(kwargs["data"])

        async with getattr(self.session, method)(uri, **kwargs) as response:
            self.response = response
            return await self._handle_response(response)

    async def _get(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return await self._request("get", path, version, **kwargs)

    async def _post(
        self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request("post", path, version, **kwargs)

    async def _put(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return await self._request("put", path, version, **kwargs)

    async def _delete(
        self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request("delete", path, version, **kwargs)

    async def get_account_balances(
        self, serialize_json_to_object: bool = False
    ) -> Dict:
        balances_json = await self._get("accountSummary")

        if serialize_json_to_object:
            return Balances(balances_json)

        return balances_json

    async def get_pairs(self, serialize_json_to_object: bool = False) -> Dict:
        pairs_json = await self._get("pairs")

        if serialize_json_to_object:
            return Pairs(pairs_json)

        return pairs_json

    async def get_price_quote(
        self,
        pair: str,
        amount: float,
        side: str,
        exchanges: str = None,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        if side != "buy" and side != "sell":
            raise NexoRequestException(
                f"Bad Request: Tried to get price quote with side = {side}, side must be 'buy' or 'sell'"
            )
        if not check_pair_validity(pair):
            raise NexoRequestException(
                f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
            )

        data = {"side": side, "amount": amount, "pair": pair}

        if exchanges:
            data["exchanges"] = exchanges

        quote_json = await self._get("quote", data=data)

        if serialize_json_to_object:
            return Quote(quote_json)

        return quote_json

    async def get_order_history(
        self,
        pairs: List[str],
        start_date: int,
        end_date: int,
        page_size: int,
        page_num: int,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        data = {
            "pairs": pairs,
            "startDate": start_date,
            "endDate": end_date,
            "pageSize": page_size,
            "pageNum": page_num,
        }
        orders_json = await self._get("orders", data=data)

        if serialize_json_to_object:
            return Orders(orders_json)

        return orders_json

    async def get_order_details(
        self, id: str, serialize_json_to_object: bool = False
    ) -> Dict:
        data = {
            "id": id,
        }

        order_details_json = await self._get(f"orderDetails", data=data)

        if serialize_json_to_object:
            return OrderDetails(order_details_json)

        return order_details_json

    async def get_trade_history(
        self,
        pairs: List[str],
        start_date: int,
        end_date: int,
        page_size: int,
        page_num: int,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        for pair in pairs:
            if not check_pair_validity(pair):
                raise NexoRequestException(
                    f"Bad Request: Tried to get trade history with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
                )

        data = {
            "pairs": pairs,
            "startDate": start_date,
            "endDate": end_date,
            "pageSize": page_size,
            "pageNum": page_num,
        }

        trades_json = await self._get("trades", data=data)

        if serialize_json_to_object:
            return TradeHistory(trades_json)

        return trades_json

    async def get_transaction_info(
        self, transaction_id: str, serialize_json_to_object: bool = False
    ) -> Dict:

        data = {"transactionId": transaction_id}

        transaction_json = await self._get(f"transaction", data=data)

        if serialize_json_to_object:
            return Transaction(transaction_json)

        return transaction_json

    async def place_order(
        self,
        pair: str,
        side: str,
        type: str,
        quantity: float,
        price: float = None,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        if side != "buy" and side != "sell":
            raise NexoRequestException(
                f"Bad Request: Tried to place an order with side = {side}, side must be 'buy' or 'sell'"
            )
        if type != "market" and type != "limit":
            raise NexoRequestException(
                f"Bad Request: Tried to place an order with type = {type}, side must be 'market' or 'limit'"
            )
        if not check_pair_validity(pair):
            raise NexoRequestException(
                f"Bad Request: Tried to place an order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
            )

        data = {"pair": pair, "side": side, "type": type, "quantity": quantity}

        if price:
            data["price"] = price

        order_id_json = await self._post("orders", data=data)

        if serialize_json_to_object:
            return OrderResponse(order_id_json)

        return order_id_json

    async def place_trigger_order(
        self,
        pair: str,
        side: str,
        trigger_type: str,
        amount: float,
        trigger_price: float,
        trailing_distance: float = None,
        trailing_percentage: float = None,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        if side != "buy" and side != "sell":
            raise NexoRequestException(
                f"Bad Request: Tried to place a trigger order with side = {side}, side must be 'buy' or 'sell'"
            )
        if (
            trigger_type != "stopLoss"
            and trigger_type != "takeProfit"
            and trigger_type != "trailing"
        ):
            raise NexoRequestException(
                f"Bad Request: Tried to place a trigger order with trigger type = {trigger_type}, trigger type must be 'stopLoss' or 'takeProfit' or 'trailing'"
            )
        if not check_pair_validity(pair):
            raise NexoRequestException(
                f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
            )

        data = {
            "pair": pair,
            "side": side,
            "triggerType": trigger_type,
            "amount": amount,
            "triggerPrice": trigger_price,
        }

        if trailing_distance:
            data["trailingDistance"] = trailing_distance

        if trailing_percentage:
            data["trailingPercentage"] = trailing_percentage

        order_id_json = await self._post("orders", data=data)

        if serialize_json_to_object:
            return OrderResponse(order_id_json)

        return order_id_json

    async def place_advanced_order(
        self,
        pair: str,
        side: str,
        amount: str,
        stop_loss_price: str,
        take_profit_price: str,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        if side != "buy" and side != "sell":
            raise NexoRequestException(
                f"Bad Request: Tried to place an advanced order with side = {side}, side must be 'buy' or 'sell'"
            )

        if not check_pair_validity(pair):
            raise NexoRequestException(
                f"Bad Request: Tried to place an advanced order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
            )

        data = {
            "pair": pair,
            "side": side,
            "amount": amount,
            "stopLossPrice": stop_loss_price,
            "takeProfitPrice": take_profit_price,
        }
        order_id_json = await self._post("orders", data=data)

        if serialize_json_to_object:
            return AdvancedOrderResponse(order_id_json)

        return order_id_json

    async def place_twap_order(
        self,
        pair: str,
        side: str,
        quantity: float,
        splits: int,
        execution_interval: int,
        exchanges: List[str] = None,
        serialize_json_to_object: bool = False,
    ) -> Dict:
        if side != "buy" and side != "sell":
            raise NexoRequestException(
                f"Bad Request: Tried to place a twap order with side = {side}, side must be 'buy' or 'sell'"
            )

        if not check_pair_validity(pair):
            raise NexoRequestException(
                f"Bad Request: Tried to place a twap order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
            )

        data = {
            "pair": pair,
            "side": side,
            "quantity": quantity,
            "splits": splits,
            "executionInterval": execution_interval,
        }

        if exchanges:
            data["exchanges"] = exchanges

        twap_order_json = await self._post("orders/twap", data=data)

        if serialize_json_to_object:
            return AdvancedOrderResponse(twap_order_json)

        return twap_order_json

    async def cancel_order(self, order_id: str):
        data = {"orderId": order_id}

        return await self._post("orders/cancel", data=data)

    async def cancel_all_orders(self, pair: str):
        if not check_pair_validity(pair):
            raise NexoRequestException(
                f"Bad Request: Tried to cancel all orders with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}"
            )

        data = {"pair": pair}

        return await self._post("orders/cancel/all", data=data)

    async def get_all_future_instruments(self):
        return await self._get("futures/instruments")

    async def get_future_positions(self, status: str):
        if status != "any" and status != "active" and status != "inactive":
            raise NexoRequestException(
                f"Bad Request: Tried to get future positions with status = {status}, status must be 'any', 'active' or 'inactive'"
            )

        data = {"status": status}

        return await self._get("futures/positions", data=data)

    async def place_future_order(
        self,
        instrument: str,
        position_action: str,
        position_side: str,
        type: str,
        quantity: float,
    ):
        if position_action != "open" and position_action != "close":
            raise NexoRequestException(
                f"Bad Request: Tried to place future position with position action = {position_action}, must be 'open' or 'close'"
            )

        if position_side != "long" and position_side != "short":
            raise NexoRequestException(
                f"Bad Request: Tried to place future position with position side = {position_side}, must be 'long' or 'short'"
            )

        if type != "market":
            raise NexoRequestException(
                f"Bad Request: Tried to place future position with type = {type}, must be 'market'"
            )

        data = {
            "positionAction": position_action,
            "instrument": instrument,
            "positionSide": position_side,
            "type": type,
            "quantity": quantity,
        }

        return await self._post("futures/order", data=data)

    async def close_all_future_positions(self):
        return await self._post("futures/close-all-positions")
