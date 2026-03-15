from api.base_client import BaseClient
from config.config import Config

class AuthClient(BaseClient):
    def __init__(self):
        super().__init__()
        if not Config.AUTH_API_KEY:
            raise EnvironmentError(
                "AUTH_API_KEY is not set. Add it to your .env file."
            )
        self.session.headers.update({
            "x-api-key": Config.AUTH_API_KEY   # ← this API uses x-api-key, not Bearer
        })
        # Override base_url for authenticated endpoints
        self.base_url = Config.BASE_AUTH_URL
        