import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOPIFY_STORE = os.getenv("SHOP_URL")
SHOPIFY_API_KEY = os.getenv("API_KEY")
SHOPIFU_API_PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"

def add_product(data):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products.json"
    response = requests.post(url, json=data)
    return response.json()
