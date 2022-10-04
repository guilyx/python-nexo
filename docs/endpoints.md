> :warning: **Disclaimer**: 

 > * API Documentation has yet to come

## [Nexo Pro API](https://pro.nexo.io/api-doc-pro)

### Account

* **GET** /api/v1/accountSummary (Retrieves account balances) ✔️

```python3
client.get_account_balances()
```

### Pairs

* **GET** /api/v1/pairs (Gets a list of all pairs, min and max amounts.) ✔️

```python3
client.get_pairs()
```

### Quote

* **GET** /api/v1/pairs (Gets a price quote.) ✔️

```python3
client.get_price_quote(pair="BTC/ETH", amount="1.0", side="buy")
```

### Order

* **POST** /api/v1/orders (Places an order.) ❌

```python3
client.place_order(pair="BTC/ETH", quantity="1.0", side="buy")
```

* **POST** /api/v1/orders/trigger (Places a trigger order.) ❌

```python3
client.place_trigger_order(pair="BTC/ETH", trigger_type="takeProfit", side="buy", trigger_price="15.0", amount="2.0")
```

* **POST** /api/v1/orders/advanced (Places an advanced order.) ❌

```python3
client.place_advanced_order(pair="BTC/USDT", side="buy", stop_loss_price="18000", tak_profit_price="22000", amount="0.001")
```

* **POST** /api/v1/orders/twap (Places a TWAP order.) ❌

```python3
client.place_twap_order(pair="BTC/USDT", side="buy", execution_interval="10", splits="100", quantity="0.001")
```

### History

* **GET** /api/v1/orders (Gets order history.) ✔️

```python3
client.get_order_history(pairs=["BTC/ETH", "BTC/USDT"], start_date="1232424242424", end_date="131415535356", page_size="30", page_num="3")
```

* **GET** /api/v1/orderDetails (Gets details of specific order.) ✔️

```python3
client.get_order_details(id="1324")
```

* **GET** /api/v1/trades (Retrieves trades history.) ✔️

```python3
client.get_trade_history(pairs=["BTC/ETH", "BTC/USDT"], start_date="1232424242424", end_date="131415535356", page_size="30", page_num="3")
```

* **GET** /api/v1/transactionInfo (Gets a transaction information.)

```python3
client.get_price_quote(transaction_id="22442")
```
