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

async def main():
    client = await nexo.AsyncClient.create(key, secret)
    print(await client.get_account_balances())

    await client.close_connection()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
