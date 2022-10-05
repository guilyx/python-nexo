import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nexo.response_serializers import *
import pytest

def test_base_class():
    balances_json = {
        'balances': [
            {
                'assetName': 'BTC', 
                'totalBalance': '0.00000000', 
                'availableBalance': '0.00000000', 
                'lockedBalance': '0.00000000', 
                'debt': '0.00000000', 
                'interest': '0.00000000'
            }
        ]
    }
    base = BaseSerializedResponse(balances_json)
    assert(str(base) == str(balances_json))

def test_balances():
    balances_json = {
        'balances': [
            {
                'assetName': 'BTC', 
                'totalBalance': '0.00000000', 
                'availableBalance': '0.00000000', 
                'lockedBalance': '0.00000000', 
                'debt': '0.00000000', 
                'interest': '0.00000000'
            }
        ]
    }

    balances = Balances(balances_json)

    assert(len(balances.balances) == 1)
    assert(balances.balances[0].asset_name == "BTC")
    assert(balances.balances[0].total_balance == "0.00000000")
    assert(balances.balances[0].available_balance == "0.00000000")
    assert(balances.balances[0].locked_balance == "0.00000000")
    assert(balances.balances[0].interest == "0.00000000")
    assert(balances.balances[0].debt == "0.00000000")

    balances_json = {
        'balances': [
            {
                'assetName': 'XRP', 
                'totalBalance': '100.0',
                'availableBalance': '2.0',
                'lockedBalance': '0.3',
                'interest': '0.4'
            }
        ]
    }

    balances = Balances(balances_json)

    assert(len(balances.balances) == 1)
    assert(balances.balances[0].asset_name == "XRP")
    assert(balances.balances[0].total_balance == "100.0")
    assert(balances.balances[0].available_balance == "2.0")
    assert(balances.balances[0].locked_balance == "0.3")
    assert(balances.balances[0].interest == "0.4")

    with pytest.raises(AttributeError):
        assert(balances.balances[0].debt == "3.0")

def test_pairs():
    pairs_json = {
        'pairs': ['BNB/USDT', 'MKR/BTC'],
        'minLimits': {
            'BNB/USDT': 0.355,
            'MKR_BTC': 0.002
        },
        'maxLimits': {
            'BNB/USDT': 3435.5,
            'MKR_BTC': 42.4
        }
    }

    pairs = Pairs(pairs_json)
    assert(len(pairs.pairs) == 2)
    assert(pairs.pairs[0] == 'BNB/USDT')
    assert(pairs.pairs[1] == 'MKR/BTC')
    assert(pairs.min_limits['BNB/USDT'] == 0.355)

    pairs_json = {
        'pairs': ['BNB/USDT', 'MKR/BTC'],
        'min_limits': {
            'BNB/USDT': 0.355,
            'MKR_BTC': 0.002
        },
        'max_limits': {
            'BNB/USDT': 3435.5,
            'MKR_BTC': 42.4
        }
    }

    pairs = Pairs(pairs_json)

    with pytest.raises(AttributeError):
        assert(pairs.min_limits == {'BNB/USDT': 0.355, 'MKR_BTC': 0.002})

    with pytest.raises(AttributeError):
        assert(pairs.max_limits == {'BNB/USDT': 3435.5, 'MKR_BTC': 42.4})

def test_quote():
    quote_json = {
        'pair': 'BNB/USDT',
        'amount': "1000.0",
        'price': "10.0",
        'timestamp': "123424243",
        'random': "34343"
    }
    
    quote = Quote(quote_json)

    assert(quote.pair == 'BNB/USDT')
    assert(quote.amount == '1000.0')
    assert(quote.price == '10.0')
    assert(quote.timestamp == "123424243")

    with pytest.raises(AttributeError):
        assert(quote.random == "34343")


def test_trade_for_order():
    trade_json = {
        "id": "234",
        "symbol": "NEXO/USDT",
        "type": "market",
        "orderAmount": "100",
        "amountFilled": "100",
        "executedPrice": "1.324",
        "timestamp": 1314242424,
        "status": "completed",
        "random": "random"
    }

    trade = TradeForOrder(trade_json)

    assert(trade.id == "234")
    assert(trade.symbol == "NEXO/USDT")
    assert(trade.type == "market")
    assert(trade.order_amount == "100")
    assert(trade.amount_filled == "100")
    assert(trade.executed_price == "1.324")
    assert(trade.timestamp == 1314242424)
    assert(trade.status == "completed")

    with pytest.raises(AttributeError):
        assert(trade.random == "random")

def test_order_details():
    order_det_json = {
        "id": "234",
        "pair": "NEXO/USDT",
        "side": "buy",
        "quantity": "100",
        "exchangeRate": "100",
        "exchangeQuantity": "1.324",
        "timestamp": 1314242424,
        "status": "completed",
        "random": "random",
        "trades": [
            {
                "id": "234",
                "symbol": "NEXO/USDT",
                "type": "market",
                "orderAmount": "100",
                "amountFilled": "100",
                "executedPrice": "1.324",
                "timestamp": 1314242424,
                "status": "completed",
                "random": "random"
            },
            {
                "id": "237",
                "symbol": "NEXO/USDT",
                "type": "market",
                "orderAmount": "100",
                "amountFilled": "100",
                "executedPrice": "1.324",
                "timestamp": 1314242424,
                "status": "completed",
                "random": "random"
            }
        ]
    }

    order_details = OrderDetails(order_det_json)

    assert(len(order_details.trades) == 2)
    assert(order_details.trades[0].id == "234")
    assert(order_details.trades[0].symbol == "NEXO/USDT")
    assert(order_details.trades[0].type == "market")
    assert(order_details.trades[0].order_amount == "100")
    assert(order_details.trades[0].amount_filled == "100")
    assert(order_details.trades[0].executed_price == "1.324")
    assert(order_details.trades[0].timestamp == 1314242424)
    assert(order_details.trades[0].status == "completed")

    assert(order_details.trades[0].id == "237")
    assert(order_details.trades[0].symbol == "NEXO/USDT")
    assert(order_details.trades[0].type == "market")
    assert(order_details.trades[0].order_amount == "100")
    assert(order_details.trades[0].amount_filled == "100")
    assert(order_details.trades[0].executed_price == "1.324")
    assert(order_details.trades[0].timestamp == 1314242424)
    assert(order_details.trades[0].status == "completed")

    with pytest.raises(AttributeError):
        assert(order_details.random == "random")

    assert(order_details.id == "234")
    assert(order_details.side == "buy")
    assert(order_details.exchange_rate == "100")
    assert(order_details.exchange_quantity == "1.324")
    assert(order_details.timestamp == 1314242424)
    assert(order_details.status == "completed")

    with pytest.raises(AttributeError):
        assert(order_details.random == "random")
