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
instruments = client.get_all_future_instruments()
print(instruments)

positions = client.get_future_positions(status="any")
print(positions)

print(client.close_all_future_positions())