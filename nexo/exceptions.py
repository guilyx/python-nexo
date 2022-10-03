import json

NEXO_API_ERROR_CODES = {
    100: "API-Key is malformed or invalid.",
    101: "Request signature is malformed or invalid.",
    102: "Some request field is malformed or missing.",
    103: "Unauthorized.",
    104: "Websocket method is invalid.",
    105: "Websocket session is already authenticated.",
    106: "Request nonce is malformed or invalid.",
    203: "No results found for specified query.",
    206: "Internal error.",
    300: "The given exchanges are unsupported for said pair.",
    301: "Rate limit exceeded.",
}

class NexoAPIException(Exception):
    def __init__(self, status_code: int, response: str):
        self.code = 0
        try:
            json_res = json.loads(response)
        except ValueError:
            self.message = 'Invalid JSON error message from Nexo: {}'.format(response.text)
        else:
            self.code = json_res['errorCode']
            self.message = json_res['errorMessage']
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return f'APIError(code={self.code}): {self.message}, {NEXO_API_ERROR_CODES[self.code]}'

class NexoRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'NexoRequestException: %s' % self.message

class NotImplementedException(Exception):
    def __init__(self, value):
        message = f'Not implemented: {value}'
        super().__init__(message)
