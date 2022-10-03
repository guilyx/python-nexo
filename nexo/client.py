from typing import Dict, Optional, List, Tuple
import hmac
import hashlib
from operator import itemgetter
import aiohttp
import base64
import urllib3
import requests
import asyncio
import json
import time
from nexo.exceptions import NexoAPIException, NEXO_API_ERROR_CODES, NexoRequestException
from nexo.helpers import check_pair_validity, compact_json_dict

class BaseClient:

    API_URL = "https://pro-api.nexo.io"
    PUBLIC_API_VERSION = "v1"

    REQUEST_TIMEOUT: float = 10

    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.timestamp_offset = 0
        self.session = self._init_session()
    
    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-nexo',
                   'Content-Type': 'application/json',
                   'X-API-KEY': self.API_KEY,
        }

        session.headers.update(headers)
        return session

    def _create_path(self, path: str, api_version: str = PUBLIC_API_VERSION):
        return f'/api/{api_version}/{path}'
        
    def _create_api_uri(self, path: str) -> str:
        return f"{self.API_URL}{path}"
    
    @staticmethod
    def _get_params_for_sig(data: Dict) -> str:
        return '&'.join(["{}={}".format(key, data[key]) for key in data])
    
    def _generate_signature(self, nonce: str,) -> str:
        m = hmac.new(self.API_SECRET.encode('utf-8'), str(nonce).encode('utf-8'), hashlib.sha256)
        return base64.b64encode(m.digest())
    
    @staticmethod
    def _order_params(data: Dict) -> List[Tuple[str, str]]:
        """Convert params to list
        :param data:
        :return:
        """
        data = dict(filter(lambda el: el[1] is not None, data.items()))
        params = []
        for key, value in data.items():
            params.append((key, str(value)))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        return params
    
    def _get_request_kwargs(self, method, force_params: bool = False, **kwargs) -> Dict:

        # set default requests timeout
        # kwargs['timeout'] = self.REQUEST_TIMEOUT

        data = kwargs.get('data', None)

        if data and isinstance(data, dict):
            kwargs['data'] = data

        # generate signature
        # kwargs['data']['timestamp'] = int(time.time() * 1000 + self.timestamp_offset)
        # kwargs['data']['signature'] = self._create_hmac_signature(kwargs['data'])

        # sort get and post params to match signature order
        if data:
            # sort post params and remove any arguments with values of None
            kwargs['data'] = self._order_params(kwargs['data'])
            # Remove any arguments with values of None.
            null_args = [i for i, (key, value) in enumerate(kwargs['data']) if value is None]
            for i in reversed(null_args):
                del kwargs['data'][i]

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del(kwargs['data'])

        return kwargs
        

class Client(BaseClient):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
    
    @staticmethod
    def _handle_response(response: requests.Response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        json_response = response.json()
        try:
            if "errorCode" in json_response:
                if json_response["errorCode"] in NEXO_API_ERROR_CODES:
                    raise NexoAPIException(json_response["errorCode"], response.text)
                else:
                    raise NexoRequestException(f'Invalid Response: status: {json_response["errorCode"]}, message: {json_response["errorMessage"]}')
            return json_response
        except ValueError:
            raise NexoRequestException('Invalid Response: %s' % json_response)
    
    def _request(
        self, method, path: str, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        # set default requests timeout
        kwargs['timeout'] = 10

        kwargs['data'] = kwargs.get('data', {})
        kwargs['headers'] = kwargs.get('headers', {})

        full_path = self._create_path(path, version)
        uri = self._create_api_uri(full_path)

        nonce = str(int(time.time() * 1000))
        kwargs['headers']['X-NONCE'] = nonce
        kwargs['headers']['X-SIGNATURE'] = self._generate_signature(nonce)

        if kwargs['data'] and method == 'get':
            kwargs['params'] = kwargs['data']
            del kwargs['data']

        if method != 'get' and kwargs['data']:
            kwargs['data'] = compact_json_dict(kwargs['data'])

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _get(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return self._request('get', path, version, **kwargs)

    def _post(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request('post', path, version, **kwargs)

    def _put(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request('put', path, version, **kwargs)

    def _delete(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request('delete', path, version, **kwargs)

    def get_account_balances(self) -> Dict:
        balances = self._get('accountSummary')
        return balances
    
    def get_pairs(self) -> Dict:
        pairs = self._get('pairs')
        return pairs
    
    def get_price_quote(self, pair: str, amount: float, side: str, exchanges: str = None) -> Dict:
        if side != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to get price quote with side = {side}, side must be 'buy' or 'sell'")
        if not check_pair_validity(pair):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")
        
        data = {
            "side": side,
            "amount": amount,
            "pair": pair
        }

        if exchanges:
            data["exchanges"] = exchanges

        quote = self._get('quote', data=data)
        return quote
    
    def get_order_history(self, pairs: List[str], start_date: int, end_date: int, page_size: int, page_num: int) -> Dict:
        data = {
            "pairs": pairs,
            "startDate": start_date,
            "endDate": end_date,
            "pageSize": page_size,
            "pageNum": page_num
        }
        orders = self._get('orders', data=data)
        return orders

    def get_order_details(self, id: str) -> Dict:
        order_details = self._get(f'orderDetails/{id}')
        return order_details

    def get_trade_history(self,  pairs: List[str], start_date: int, end_date: int, page_size: int, page_num: int) -> Dict:
        for pair in pairs:
            if not check_pair_validity(pair):
                raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")
        
        data = {
            "pairs": pairs,
            "startDate": start_date,
            "endDate": end_date,
            "pageSize": page_size,
            "pageNum": page_num
        }
        trades = self._get('trades', data=data)
        return trades
    
    def get_transaction_info(self, transaction_id: str) -> Dict:
        transaction = self._get(f'transaction/{transaction_id}')
        return transaction

    def place_order(self, pair: str, side: str, type: str, quantity: float, price: float = None) -> Dict:
        if side != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place an order with side = {side}, side must be 'buy' or 'sell'")
        if type != "market" and "limit":
            raise NexoRequestException(f"Bad Request: Tried to place an order with type = {type}, side must be 'market' or 'limit'")
        if not check_pair_validity(pair):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        data = {
            "pair": pair,
            "side": side,
            "type": type,
            "quantity": quantity
        }

        if price:
            data["price"] = price

        order_id = self._post('orders', data=data)
        return order_id
    
    def place_trigger_order(self, pair: str, side: str, trigger_type: str, amount: float, trigger_price: float, trailing_distance: float = None, trailing_percentage: float = None) -> Dict:
        if side != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with side = {side}, side must be 'buy' or 'sell'")
        if trigger_type != "stopLoss" and "takeProfit" and "trailing":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with type = {trigger_type}, side must be 'market' or 'limit'")
        if not check_pair_validity(pair):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        data = {
            "pair": pair,
            "side": side,
            "triggerType": trigger_type,
            "amount": amount,
            "triggerPrice": trigger_price
        }

        if trailing_distance:
            data["trailingDistance"] = trailing_distance
        
        if trailing_percentage:
            data["trailingPercentage"] = trailing_percentage

        order_id = self._post('orders', data=data)
        return order_id
    
    def place_advanced_order(self, pair: str, side: str, amount: str, stopLossPrice: str, takeProfitPrice: str) -> Dict:
        if side != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with side = {side}, side must be 'buy' or 'sell'")

        if not check_pair_validity(pair):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        data = {
            "pair": pair,
            "side": side,
            "amount": amount,
            "stopLossPrice": stopLossPrice,
            "takeProfitPrice": takeProfitPrice
        }
        order_id = self._post('orders', data=data)
        return order_id
    
    def place_twap_order(self, pair: str, side: str, quantity: float, exchanges: List[str], splits: int, execution_interval: int) -> Dict:
        if side != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with side = {side}, side must be 'buy' or 'sell'")

        if not check_pair_validity(pair):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        data = {
            "pair": pair,
            "side": side,
            "quantity": quantity,
            "exchanges": exchanges,
            "splits": splits,
            "executionInterval": execution_interval
        }

        twap_order = self._post('orders/twap', data=data)

        return twap_order