import sys
from os import path
import time

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import nexo
import os
from dotenv import load_dotenv

import time

load_dotenv()

key = os.getenv("NEXO_PUBLIC_KEY")
secret = os.getenv("NEXO_SECRET_KEY")

client = nexo.Client(key, secret)
hist = client.get_order_history(["ATOM/USDT", "ETH/USDT"], 0, None, None, None)
print(hist)
