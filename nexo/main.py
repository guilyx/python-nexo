if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from client import Client
    load_dotenv()

    nexo_key = os.getenv("NEXO_PUBLIC_KEY")
    nexo_secret = os.getenv("NEXO_SECRET_KEY")

    assert(nexo_key)
    assert(nexo_secret)

    c = Client(nexo_key, nexo_secret)
    balances = c.place_order(pair="BTC/BSD", side="buy", type="market", quantity=10.0, price=30.0)
    print(balances)