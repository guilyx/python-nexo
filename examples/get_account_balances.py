import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import nexo
import os
from dotenv import load_dotenv

import time

load_dotenv()

key = os.getenv("NEXO_PUBLIC_KEY")
secret = os.getenv("NEXO_SECRET_KEY")

client = nexo.Client(key, secret)
balances = client.get_account_balances()
print(balances)
