import requests
from config import Config
from utils.assertions import check_rate_limit

class BaseClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
        self.base_url = Config.BASE_URL

    def _send(self, method, endpoint, **kwargs):
        """
        Central method that all HTTP methods route through.
        Checks for rate limiting on every response.
        """
        response = self.session.request(
            method,
            f"{self.base_url}{endpoint}",
            timeout=Config.TIMEOUT,
            **kwargs
        )
        check_rate_limit(response)
        return response

    def get(self, endpoint, **kwargs):
        return self._send("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._send("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._send("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._send("DELETE", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._send("PATCH", endpoint, **kwargs)
    