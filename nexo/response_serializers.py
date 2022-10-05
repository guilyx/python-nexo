from typing import Dict


class BaseSerializedResponse:
    def __init__(self, json_dictionary: Dict):
        self.json_dictionary = json_dictionary

    def __repr__(self):
        return str(self.json_dictionary)


# GET /balances
class WalletBalance(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "assetName" in json_dictionary:
            self.asset_name = json_dictionary["assetName"]
        if "totalBalance" in json_dictionary:
            self.total_balance = json_dictionary["totalBalance"]
        if "availableBalance" in json_dictionary:
            self.available_balance = json_dictionary["availableBalance"]
        if "lockedBalance" in json_dictionary:
            self.locked_balance = json_dictionary["lockedBalance"]
        if "debt" in json_dictionary:
            self.debt = json_dictionary["debt"]
        if "interest" in json_dictionary:
            self.interest = json_dictionary["interest"]


class Balances(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "balances" in json_dictionary:
            self.balances = [
                WalletBalance(balance) for balance in json_dictionary["balances"]
            ]


# GET /pairs
class Pairs(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "pairs" in json_dictionary:
            self.pairs = json_dictionary["pairs"]
        if "minLimits" in json_dictionary:
            self.min_limits = json_dictionary["minLimits"]
        if "maxLimits" in json_dictionary:
            self.max_limits = json_dictionary["maxLimits"]


# GET /quote
class Quote(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "pair" in json_dictionary:
            self.pair = json_dictionary["pair"]
        if "amount" in json_dictionary:
            self.amount = json_dictionary["amount"]
        if "price" in json_dictionary:
            self.price = json_dictionary["price"]
        if "timestamp" in json_dictionary:
            self.timestamp = json_dictionary["timestamp"]


# POST /orders | /orders/trigger | /orders/advanced
class OrderResponse(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "orderId" in json_dictionary:
            self.order_id = json_dictionary["orderId"]


# POST /orders/twap
class AdvancedOrderResponse(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "orderId" in json_dictionary:
            self.order_id = json_dictionary["orderId"]

        if "amount" in json_dictionary:
            self.amount = json_dictionary["amount"]


class TradeForOrder(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "id" in json_dictionary:
            self.id = json_dictionary["id"]
        if "symbol" in json_dictionary:
            self.symbol = json_dictionary["symbol"]
        if "type" in json_dictionary:
            self.type = json_dictionary["type"]
        if "orderAmount" in json_dictionary:
            self.order_amount = json_dictionary["orderAmount"]
        if "amountFilled" in json_dictionary:
            self.amount_filled = json_dictionary["amountFilled"]
        if "executedPrice" in json_dictionary:
            self.executed_price = json_dictionary["executedPrice"]
        if "timestamp" in json_dictionary:
            self.timestamp = json_dictionary["timestamp"]
        if "status" in json_dictionary:
            self.status = json_dictionary["status"]


# GET /orderDetails
class OrderDetails(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "id" in json_dictionary:
            self.id = json_dictionary["id"]
        if "side" in json_dictionary:
            self.side = json_dictionary["side"]
        if "pair" in json_dictionary:
            self.pair = json_dictionary["pair"]
        if "timestamp" in json_dictionary:
            self.timestamp = json_dictionary["timestamp"]
        if "quantity" in json_dictionary:
            self.quantity = json_dictionary["quantity"]
        if "exchangeRate" in json_dictionary:
            self.exchange_rate = json_dictionary["exchangeRate"]
        if "exchangeQuantity" in json_dictionary:
            self.exchange_quantity = json_dictionary["exchangeQuantity"]
        if "trades" in json_dictionary:
            self.trades = [TradeForOrder(trade) for trade in json_dictionary["trades"]]


# GET /orders
class Orders(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "orders" in json_dictionary:
            self.orders = [OrderDetails(order) for order in json_dictionary["orders"]]


# GET /trades
class Trade(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "id" in json_dictionary:
            self.id = json_dictionary["id"]
        if "symbol" in json_dictionary:
            self.symbol = json_dictionary["symbol"]
        if "side" in json_dictionary:
            self.side = json_dictionary["side"]
        if "tradeAmount" in json_dictionary:
            self.trade_amount = json_dictionary["tradeAmount"]
        if "executedPrice" in json_dictionary:
            self.executed_price = json_dictionary["executedPrice"]
        if "timestamp" in json_dictionary:
            self.timestamp = json_dictionary["timestamp"]
        if "orderId" in json_dictionary:
            self.order_id = json_dictionary["orderId"]


class TradeHistory(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "trades" in json_dictionary:
            self.trades = [Trade(trade) for trade in json_dictionary["trades"]]


class Transaction(BaseSerializedResponse):
    def __init__(self, json_dictionary: Dict):
        super().__init__(json_dictionary)

        if "transactionId" in json_dictionary:
            self.transaction_id = json_dictionary["transactionId"]
        if "createDate" in json_dictionary:
            self.create_date = json_dictionary["createDate"]
        if "assetName" in json_dictionary:
            self.asset_name = json_dictionary["assetName"]
        if "amount" in json_dictionary:
            self.amount = json_dictionary["amount"]
        if "type" in json_dictionary:
            self.type = json_dictionary["type"]
        if "status" in json_dictionary:
            self.status = json_dictionary["status"]
