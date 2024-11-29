<div align="center">

# Unofficial Nexo API Wrapper (Python)

✨ A Python wrapper for the Nexo Pro API ✨

</div>

<div align="center">
    
![lint](https://github.com/guilyx/python-nexo/workflows/lint/badge.svg?branch=master)
[![tests](https://github.com/guilyx/python-nexo/actions/workflows/tests.yml/badge.svg)](https://github.com/guilyx/python-nexo/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/guilyx/python-nexo/branch/master/graph/badge.svg?token=GXUOT9P1WE)](https://codecov.io/gh/guilyx/python-nexo)
[![CodeFactor](https://www.codefactor.io/repository/github/guilyx/python-nexo/badge)](https://www.codefactor.io/repository/github/guilyx/python-nexo)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/guilyx/python-nexo.svg)](http://isitmaintained.com/project/guilyx/python-nexo "Percentage of issues still open")
![PipPerMonths](https://img.shields.io/pypi/dm/python-nexo.svg)
[![Pip version fury.io](https://badge.fury.io/py/python-nexo.svg)](https://pypi.python.org/pypi/python-nexo/)
[![GitHub license](https://img.shields.io/github/license/guilyx/python-nexo.svg)](https://github.com/guilyx/python-nexo/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/guilyx/python-nexo.svg)](https://GitHub.com/guilyx/python-nexo/graphs/contributors/)

</div>

<div align="center">
    
[Report Bug](https://github.com/guilyx/python-nexo/issues) · [Request Feature](https://github.com/guilyx/python-nexo/issues)

</div>

## About Nexo 💸

Nexo is a crypto lending platform that lets you borrow crypto or cash by placing your crypto as collateral. They offer high APY on holdings based on loyalty tier (the more Nexo token you hold the higher your tier). You can earn your interests in the same kind of your holding or as Nexo tokens. As an example, stablecoins can earn up to 12% APY. Bitcoin and Ethereum, 8%. 

Unfortunately, Nexo doesn't offer some automated way of buying periodically. All you can do is setup a bank transfer and then convert/buy manually. This API Wrapper aims to offer a way of automating your purchases. You'd just have to setup your periodic bank transfer to Nexo, and then buy at spot price the coins that you want in an automated way by using the wrapped API calls.

## Description 📰

This is an unofficial Python wrapper for the Nexo Pro exchange REST API v1. I am in no way affiliated with Nexo, use at your own risk.

If you came here looking for the Nexo exchange to purchase cryptocurrencies, then go to the official Nexo website. If you want to automate interactions with Nexo, stick around.

[Click here to register a Nexo account](https://nexo.io/ref/vaqo55u5py?src=web-link)

Heavily influenced by [python-binance](https://github.com/sammchardy/python-binance)

You can check which endpoints are currently functional [here](https://github.com/guilyx/python-nexo/blob/master/docs/endpoints.md)

- ✨ Work in Progress
- 🎌 Built with Python
- 🐋 Docker Available
- 🍻 Actively Maintained

## Roadmap 🌱

See it on Issue https://github.com/guilyx/python-nexo/issues/2
Checkout the [Changelog](https://github.com/guilyx/python-nexo/blob/master/docs/changelog.md)

## Preparation 🔎

- Register a Nexo Account. [here](https://nexo.io/ref/vaqo55u5py?src=web-link)
- Generate an API Key in Nexo Pro with the permissions you want.

## Advice

Priviledge Async Client. The advantage of async processing is that we don’t need to block on I/O which is every action that we make when we interact with the Nexo Pro servers.

By not blocking execution we can continue processing data while we wait for responses or new data from websockets.

## Set it up 💾

### PIP

1. Install the pip package: `python3 -m pip install python-nexo`
2. Explore the API:

```python3
#### Sync

import nexo
import os
from dotenv import load_dotenv

# Loads your API keys from the .env file you created
load_dotenv()
key = os.getenv("NEXO_PUBLIC_KEY")
secret = os.getenv("NEXO_SECRET_KEY")

# Instantiate Client and grab account balances
c = nexo.Client(key, secret)
balances = c.get_account_balances()
print(balances)

#### Async

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
```

### Docker (source)

1. Clone the Project: `git clone -b master https://github.com/guilyx/python-nexo.git`
2. Move to the Repository: `cd python-nexo`
3. Create a copy of `.env.example` and name it `.env`
4. Fill up your API Key/Secret
5. Build and Compose the Docker: `docker-compose -f docker/docker-compose.yml up` - The container should keep running so that you can explore the API
6. Attach to the docker: `docker exec -it $(docker ps -qf "name=docker_python-nexo") /bin/bash`
7. Run python in the docker's bash environment: `python3`
8. From there, copy the following snippet to instantiate a Client:

```python3
import nexo
import os
nexo_key = os.getenv("NEXO_PUBLIC_KEY")
nexo_secret = os.getenv("NEXO_SECRET_KEY")
assert(nexo_key)
assert(nexo_secret)
c = nexo.Client(nexo_key, nexo_secret)
```

9. You can now explore the client's exposed endpoints, for instance:

```python3
balances = c.get_account_balances()
print(balances)
```

## Contribute 🆘

Open an issue to state clearly the contribution you want to make. Upon aproval send in a PR with the Issue referenced. (Implement Issue #No / Fix Issue #No).

## Maintainers Ⓜ️

- Erwin Lejeune

## Buy me a Coffee

*ERC-20 / EVM: **0x07ed706146545d01fa66a3c08ebca8c93a0089e5***

*BTC: **bc1q3lu85cfkrc20ut64v90y428l79wfnv83mu72jv***

*DOT: **1Nt7G2igCuvYrfuD2Y3mCkFaU4iLS9AZytyVgZ5VBUKktjX***

*DAG: **DAG7rGLbD71VrU6nWPrepdzcyRS6rFVvfWjwRKg5***

*LUNC: **terra12n3xscq5efr7mfd6pk5ehtlsgmaazlezhypa7g***
