import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import nexo
import os
from dotenv import load_dotenv


load_dotenv()

key = os.getenv("NEXO_PUBLIC_KEY")
secret = os.getenv("NEXO_SECRET_KEY")

client = nexo.Client(key, secret)

# Buys 0.03 ETH with USDT at market price
order_resp = client.place_order(
    "ETH/USDT", "buy", "market", "0.03", serialize_json_to_object=True
)
print(order_resp)

# Gets order details
order = client.get_order_details(str(order_resp.order_id))
print(order)

# Sells 0.03 ETH for USDT at limit price 2000 USDT
order_resp = client.place_order(
    "ETH/USDT", "sell", "limit", "0.03", "1500", serialize_json_to_object=True
)
print(order_resp)

cancel_order = client.cancel_all_orders("ETH/USDT")
print(cancel_order)

print(client.cancel_order("kerar"))
