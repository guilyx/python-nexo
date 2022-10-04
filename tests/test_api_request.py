import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pytest
import nexo

client = nexo.Client("key", "secret")

def test_client():
    assert(client.API_KEY == "key")
    assert(client.API_SECRET == "secret")

def test_forbidden_call():
    with pytest.raises(nexo.NexoAPIException) as e:
        client.get_account_balances()

    assert(e.value.code == 100)
    assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")

def test_get_trade_history_validity():
    pair = "IDONTEXIST"
    with pytest.raises(nexo.NexoRequestException) as e:
        client.get_trade_history([pair], None, None, None, None)
    
    assert(e.value.message == f"Bad Request: Tried to get trade history with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

    pair = "ETH/USDT"
    with pytest.raises(nexo.NexoAPIException) as e:
        client.get_trade_history([pair], None, None, None, None)

    assert(e.value.code == 100)
    assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")

def test_place_order_wrong_pair():
    pair = "ETHUSDT"
    with pytest.raises(nexo.NexoRequestException) as e:
        client.place_order(pair, "buy", "market", "10.0")
    
    assert(e.value.message == f"Bad Request: Tried to place an order with pair = {pair}, must be of format [A-Z]{{2,6}}/[A-Z]{{2, 6}}")

def test_place_order_wrong_type():
    type = "int"
    with pytest.raises(nexo.NexoRequestException) as e:
        client.place_order("ETH/USDT", "buy", type, "10.0")
    
    assert(e.value.message == f"Bad Request: Tried to place an order with type = {type}, side must be 'market' or 'limit'")

def test_place_order_wrong_side():
    side = "tails"
    with pytest.raises(nexo.NexoRequestException) as e:
        client.place_order("ETH/USDT", side, "market", "10.0")
    
    assert(e.value.message == f"Bad Request: Tried to place an order with side = {side}, side must be 'buy' or 'sell'")


def test_place_order_healthy():
    pair = "ETH/USDT"
    with pytest.raises(nexo.NexoAPIException) as e:
        client.place_order(pair, "buy", "market", "10.0")
    
    assert(e.value.code == 100)
    assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")

    pair = "ETH/USDT"
    with pytest.raises(nexo.NexoAPIException) as e:
        client.place_order(pair, "sell", "market", "10.0")
    
    assert(e.value.code == 100)
    assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")
    
    pair = "ETH/USDT"
    with pytest.raises(nexo.NexoAPIException) as e:
        client.place_order(pair, "buy", "limit", "10.0")
    
    assert(e.value.code == 100)
    assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")

    pair = "ETH/USDT"
    with pytest.raises(nexo.NexoAPIException) as e:
        client.place_order(pair, "sell", "limit", "10.0")
    
    assert(e.value.code == 100)
    assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")
    
    
    