import os
from utils import get_infos 
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


data = get_infos()
url = f"{BASE_URL}/admin/api/{API_VERSION}/products.json"
response = requests.post(url, json=data)
print(response.raise_for_status())