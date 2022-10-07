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
quote = client.get_price_quote("ETH/USDT", "100.0", "buy")
print(quote)