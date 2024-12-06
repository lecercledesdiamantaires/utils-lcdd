import os
from dotenv import load_dotenv
import os





load_dotenv()

SHOPIFY_API_KEY = os.getenv("API_KEY")
SHOPIFU_API_PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE")

