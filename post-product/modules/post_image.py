import requests
import time
import os
import logging

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE = os.getenv("SHOP_URL")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"

logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def post_image(product_id, src, title, retries=5, delay=10):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images.json"
    data = {
        "image": {
            "src": src,
            "alt" : title
        }
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout as e:
            return None
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Failed to post image.")
                return None
