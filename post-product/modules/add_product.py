import os
from dotenv import load_dotenv
import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]
SHOPIFY_API_KEY = st.secrets["API_KEY"]
SHOP_NAME = st.secrets["SHOP_NAME"]
API_VERSION = st.secrets["API_VERSION"]
LIMIT = st.secrets["LIMIT"]
FALSE_URL = st.secrets["FALSE_URL"]
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"

def add_product(data):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products.json"
    response = requests.post(url, json=data)
    return response.json()
