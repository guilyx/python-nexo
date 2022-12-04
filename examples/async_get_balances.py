import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import nexo
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("NEXO_PUBLIC_KEY")
secret = os.getenv("NEXO_SECRET_KEY")

client = nexo.AsyncClient.create()
print(await client.get_account_balances())
