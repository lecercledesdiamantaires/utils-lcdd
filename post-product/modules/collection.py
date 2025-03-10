import requests
import streamlit as st

API_VERSION = st.secrets["API_VERSION"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]
PASSWORD = st.secrets["PASSWORD"]

BASE_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}"

COLLECTIONS_ID = {
    "Bague": 628351533391,
    "Alliance": 628351861071,
    "Fiancailles": 628351566159,
    "Bracelet": 628351631695,
    "Collier": 628351697231,
    "Boucles d'oreilles": 628351598927,
    "Broche": 628352057679,
    "Catalogue": 658578145615,
}

def collection(product_category, product_id):
    if product_category in ["Puce", "Pendantes"]:
        product_category = "Boucles d'oreilles"

    if product_category in ["Bague Catalogue", "Collier Catalogue", "Bracelet Catalogue", "Boucles doreilles Catalogue"]:
        product_category = "Catalogue"

    url = f"{BASE_URL}/collects.json"

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": PASSWORD
    }

    if product_category == "Alliance":
        for cat in ["Bague", "Fiancailles"]:
            data = {
                "collect": {
                    "collection_id": COLLECTIONS_ID[cat],
                    "product_id": product_id
                }
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code != 201:
                print(f"Erreur {response.status_code} pour {cat}: {response.text}")

    if product_category in COLLECTIONS_ID:
        data = {
            "collect": {
                "collection_id": COLLECTIONS_ID[product_category],
                "product_id": product_id
            }
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code != 201:
            print(f"Erreur {response.status_code} pour {product_category}: {response.text}")
