from typing import Dict, Optional, List, Tuple
import hmac
import hashlib
import requests
from operator import itemgetter
import aiohttp
import urllib3
import asyncio
import json
import time
from nexo.exceptions import NexoAPIException, NEXO_API_ERROR_CODES, NexoRequestException
from nexo.helpers import check_pair_validity

class BaseClient:

    API_URL = "https://pro-api.nexo.io/api"
    PUBLIC_API_VERSION = "v1"

    REQUEST_TIMEOUT: float = 10

    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.timestamp_offset = 0
        
    def _create_api_uri(self, path: str, version: str = PUBLIC_API_VERSION) -> str:
        url = self.API_URL
        return url + '/' + version + '/' + path
    
    def _generate_signature(self, data: Dict) -> str:
        assert self.API_SECRET, "API Secret required for private endpoints"
        ordered_data = self._order_params(data)
        query_string = '&'.join([f"{d[0]}={d[1]}" for d in ordered_data])
        m = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return m
    
    def _get_headers(self, url: str, payload: Dict) -> Dict:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',  # noqa
        }
        
        headers['X-API-KEY'] = self.API_KEY
        headers['X-NONCE'] = int(time.time() * 1000 + self.timestamp_offset)
        headers['X-SIGNATURE'] = self._generate_signature(payload)
        print(payload)
        return headers
    
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
    def _handle_response(response: urllib3.HTTPResponse):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        json_response = json.loads(response.data)
        try:
            if "errorCode" in json_response:
                if json_response["errorCode"] in NEXO_API_ERROR_CODES:
                    raise NexoAPIException(json_response["errorCode"], response.data)
                else:
                    raise NexoRequestException(f'Invalid Response: status: {json_response["errorCode"]}, message: {json_response["errorMessage"]}')
            return json_response
        except ValueError:
            raise NexoRequestException('Invalid Response: %s' % json_response)
    
    def _request(self, method, uri: str, **kwargs):

        kwargs = self._get_request_kwargs(method, **kwargs)
        http = urllib3.PoolManager()
        if method == "get" or method == "delete" or method == "head" or method == "options":
            self.response = http.request(method=method.upper(), fields=kwargs, url=uri, headers=self._get_headers(url=f"{uri}", payload=kwargs))
        else:
            self.response = http.request_encode_body(method=method.upper(), fields=kwargs, url=uri, headers=self._get_headers(url=f"{uri}", payload=kwargs), encode_multipart=False)
        
        return self._handle_response(self.response)

    def _request_api(
        self, method, path: str, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        uri = self._create_api_uri(path, version)
        return self._request(method, uri, **kwargs)
    
    def _get(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return self._request_api('get', path, version, **kwargs)

    def _post(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request_api('post', path, version, **kwargs)

    def _put(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request_api('put', path, version, **kwargs)

    def _delete(self, path, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request_api('delete', path, version, **kwargs)

    def get_account_balances(self):
        balances = self._request_api('get', 'accountSummary')
        return balances
    
    def get_pairs(self):
        pairs = self._request_api('get', 'pairs')
        return pairs
    
    def get_price_quote(self, **kwargs):
        if not "pair" in kwargs:
            raise NexoRequestException(f"Bad Request: [pair] is a required parameter")
        
        if not "amount" in kwargs:
            raise NexoRequestException(f"Bad Request: [amount] is a required parameter")
        
        if not "side" in kwargs:
            raise NexoRequestException(f"Bad Request: [side] is a required parameter")
        
        if kwargs["side"] != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to get price quote with side = {kwargs['side']}, side must be 'buy' or 'sell'")
        if not check_pair_validity(kwargs["pair"]):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {kwargs['pair']}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        quote = self._request_api('get', 'quote', **kwargs)
        return quote
    
    def get_order_history(self):
        orders = self._request_api('get', 'orders')
        return orders

    def get_order_details(self, **kwargs):
        if not "id" in kwargs:
            raise NexoRequestException(f"Bad Request: [id] is a required parameter")

        order_details = self._request_api('get', 'orderDetails', **kwargs)
        return order_details

    def get_trade_history(self):
        trades = self._request_api('get', 'trades')
        return trades
    
    def get_transaction_info(self, **kwargs):
        if not "transactionId" in kwargs:
            raise NexoRequestException(f"Bad Request: [transactionId] is a required parameter")

        transaction = self._request_api('get', 'transaction', **kwargs)
        return transaction

    def place_order(self, **kwargs):
        if not "pair" in kwargs:
            raise NexoRequestException(f"Bad Request: [pair] is a required parameter")
        if not "side" in kwargs:
            raise NexoRequestException(f"Bad Request: [side] is a required parameter")
        if not "type" in kwargs:
            raise NexoRequestException(f"Bad Request: [type] is a required parameter")
        if not "quantity" in kwargs:
            raise NexoRequestException(f"Bad Request: [quantity] is a required parameter")

        if kwargs["side"] != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place an order with side = {kwargs['side']}, side must be 'buy' or 'sell'")
        if kwargs["type"] != "market" and "limit":
            raise NexoRequestException(f"Bad Request: Tried to place an order with type = {kwargs['type']}, side must be 'market' or 'limit'")
        if not check_pair_validity(kwargs["pair"]):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {kwargs['pair']}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        order_id = self._request_api('post', 'orders', **kwargs)
        return order_id
    
    def place_trigger_order(self, **kwargs):
        if not "pair" in kwargs:
            raise NexoRequestException(f"Bad Request: [pair] is a required parameter")
        if not "side" in kwargs:
            raise NexoRequestException(f"Bad Request: [side] is a required parameter")
        if not "triggerType" in kwargs:
            raise NexoRequestException(f"Bad Request: [triggerType] is a required parameter")
        if not "amount" in kwargs:
            raise NexoRequestException(f"Bad Request: [amount] is a required parameter")
        if not "triggerPrice" in kwargs:
            raise NexoRequestException(f"Bad Request: [triggerPrice] is a required parameter")

        if kwargs["side"] != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with side = {kwargs['side']}, side must be 'buy' or 'sell'")
        if kwargs["triggerType"] != "stopLoss" and "takeProfit" and "trailing":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with type = {kwargs['triggerType']}, side must be 'market' or 'limit'")
        if not check_pair_validity(kwargs["pair"]):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {kwargs['pair']}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        order_id = self._request_api('post', 'orders', **kwargs)
        return order_id
    
    def place_advanced_order(self, **kwargs):
        if not "pair" in kwargs:
            raise NexoRequestException(f"Bad Request: [pair] is a required parameter")
        if not "side" in kwargs:
            raise NexoRequestException(f"Bad Request: [side] is a required parameter")
        if not "amount" in kwargs:
            raise NexoRequestException(f"Bad Request: [amount] is a required parameter")
        if not "stopLossPrice" in kwargs:
            raise NexoRequestException(f"Bad Request: [stopLossPrice] is a required parameter")
        if not "takeProfitPrice" in kwargs:
            raise NexoRequestException(f"Bad Request: [takeProfitPrice] is a required parameter")

        if kwargs["side"] != "buy" and "sell":
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with side = {kwargs['side']}, side must be 'buy' or 'sell'")

        if not check_pair_validity(kwargs["pair"]):
            raise NexoRequestException(f"Bad Request: Tried to place a trigger order with pair = {kwargs['pair']}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

        order_id = self._request_api('post', 'orders', **kwargs)
        return order_id
    
    def place_twap_order(self, **kwargs):
        twap_order = self._request_api('post', 'orders/twap', **kwargs)
        return twap_order