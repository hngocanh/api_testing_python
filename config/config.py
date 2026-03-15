import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    BASE_AUTH_URL = os.getenv("BASE_AUTH_URL")
    TIMEOUT = 10
    HEADERS = {"Content-Type": "application/json"}
    AUTH_API_KEY = os.getenv("AUTH_API_KEY")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")