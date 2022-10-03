import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pytest
import nexo

client = nexo.Client("key", "secret")

def test_client():
    assert(client.API_KEY == "key")
    assert(client.API_SECRET == "secret")

def test_forbidden_call():
        with pytest.raises(nexo.NexoAPIException) as e:
            client.get_account_balances()

        assert(e.value.code == 100)
        assert(str(e.value) == "APIError(code=100): API Key doesn't exist, API-Key is malformed or invalid.")
