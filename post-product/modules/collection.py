import os
import streamlit as st
import requests

API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]
SHOP_NAME = st.secrets["SHOP_NAME"]
API_VERSION = st.secrets["API_VERSION"]
LIMIT = st.secrets["LIMIT"]
FALSE_URL = st.secrets["FALSE_URL"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"

COLLECTIONS_ID = {
    "Bague": 628351533391,
    "Alliance": 628351861071,
    "Fiancailles": 628351566159,
    "Bracelet": 628351631695,
    "Collier": 628351697231,
    "Boucles d'oreilles": 628351598927,
    "Broche": 628352057679,
}

def collection(product_category, product_id):
    if product_category == "Puce" or product_category == "Pendantes":
        product_category = "Boucles d'oreilles"

    url = f"{BASE_URL}/admin/api/{API_VERSION}/collects.json"

    if product_category == "Alliance":
        for cat in ["Bague", "Fiancailles"]:
            data = {
                "collect": {
                    "collection_id": COLLECTIONS_ID[cat],
                    "product_id": product_id
                }
            }
            response = requests.post(url, json=data, timeout=10)
            if response.status_code != 201:
                print(f"Erreur {response.status_code} pour {cat}: {response.text}")

    # Ajout principal du produit à la collection correspondante
    if product_category in COLLECTIONS_ID:
        data = {
            "collect": {
                "collection_id": COLLECTIONS_ID[product_category],
                "product_id": product_id
            }
        }
        response = requests.post(url, json=data, timeout=10)
        if response.status_code != 201:
            print(f"Erreur {response.status_code} pour {product_category}: {response.text}")