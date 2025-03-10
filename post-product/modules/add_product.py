import os
from dotenv import load_dotenv
import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]
SHOP_NAME = st.secrets["SHOP_NAME"]
API_VERSION = st.secrets["API_VERSION"]
LIMIT = st.secrets["LIMIT"]
FALSE_URL = st.secrets["FALSE_URL"]
BASE_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}"

def add_product(data):
    url = f"{BASE_URL}/products.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": PASSWORD  
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201:
        raise Exception(f"Erreur API Shopify: {response.status_code}, {response.text}")
    
    return response.json()
