import base64
from typing import Dict, Optional, List, Tuple
import hmac
import hashlib

class BaseClient:
    API_URL = "https://pro-api.nexo.io"
    PUBLIC_API_VERSION = "v1"

    REQUEST_TIMEOUT = 10

    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.timestamp_offset = 0

    def _create_path(self, path: str, api_version: str = PUBLIC_API_VERSION):
        return f"/api/{api_version}/{path}"

    def _create_api_uri(self, path: str) -> str:
        return f"{self.API_URL}{path}"

    @staticmethod
    def _get_params_for_sig(data: Dict) -> str:
        return "&".join(["{}={}".format(key, data[key]) for key in data])

    def _generate_signature(self, nonce: str,) -> str:
        m = hmac.new(
            self.API_SECRET.encode("utf-8"), str(nonce).encode("utf-8"), hashlib.sha256
        )
        return base64.b64encode(m.digest())
