import requests
import time
import os
import logging
import streamlit as st

API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]
SHOP_NAME = st.secrets["SHOP_NAME"]
API_VERSION = st.secrets["API_VERSION"]
LIMIT = st.secrets["LIMIT"]
FALSE_URL = st.secrets["FALSE_URL"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]
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
