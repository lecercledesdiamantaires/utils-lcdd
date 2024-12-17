import requests
import time
import os

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE = os.getenv("SHOP_URL")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"

def post_image(product_id, src, retries=5, delay=10):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images.json"
    data = {
        "image": {
            "src": src,
            "alt" : "test"
        }
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            print(f"Image posted successfully: {data['image']['src']}")
            return response.json()
        except requests.exceptions.ReadTimeout as e:
            print(f"Read timeout error: {e}. Skipping this image.")
            return None
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
