import requests
from config import Config

class BaseClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
        self.base_url = Config.BASE_URL

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT, **kwargs)
                                
    def post(self, endpoint, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT, **kwargs)
                                 
    def put(self, endpoint, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT, **kwargs)
    
    def patch(self, endpoint, **kwargs):
        return self.session.patch(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT, **kwargs)
    
    