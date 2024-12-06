import csv
import json
import requests
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE = os.getenv("SHOPIFY_URL")


def get_all_products():
    products = []
    next_page_url = f"{BASE_URL}/admin/api/2023-04/products.json?limit={LIMIT}"

    while next_page_url:
        response = requests.get(next_page_url)
        response.raise_for_status()  # Vérifie s'il y a une erreur HTTP
        data = response.json()
        products.extend(data["products"])
        # Vérifier s'il y a une page suivante
        if "Link" in response.headers:
            links = response.headers["Link"]
            if 'rel="next"' in links:
                next_page_url = links.split(",")[0].split(";")[0].strip("<>").replace(FALSE_URL, f"{BASE_URL}/admin/api/2023-04/products.json")
            else:
                next_page_url = None
        else:
            next_page_url = None

    return products



def edit_product_description(description, title_product):  
    # Pattern pour extraire le contenu jusqu'à la fin de la div `infos-product`
    div_pattern = r'(<p>.*?</div>)'
    
    try:
        # Recherche du contenu correspondant au pattern
        match = re.search(div_pattern, description, re.DOTALL)

        if match:
            # Récupérer le contenu de la div
            cleaned_content = match.group(1).strip()
            
            # Ajouter le titre du produit à la description
            new_description = f"{cleaned_content}\n<p>Photos retouchées</p>"
            return new_description
        else:
            raise ValueError("La structure <div class=\"infos-product\">...</div> est manquante ou incorrecte.")
    except ValueError as e:
        print(f"Erreur : {e}")
        return description


def put_product(product_id, data):
    url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}.json"
    response = requests.put(url, json=data)
    return response.json()

# def get_product(product_id ):
#     url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}.json"
#     response = requests.get(url)
#     return response.json()

products = get_all_products()

for product in products :
    print(product['title'], product['id'])
    description = product['body_html']
    title_product = product['title']
    new_description = edit_product_description(description, title_product)
    
    data = {
        "product": {
            "id": product['id'],
            "body_html": new_description
        }
    }

    put_product(product['id'], data)

# PRODUCT_ID = 14830316323151
# product = get_product(PRODUCT_ID)
# product = product['product']
# description = product['body_html']
# title_product = product['title']

# new_description = edit_product_description(description, title_product)
    
# data = {
#     "product": {
#         "id": PRODUCT_ID,
#         "body_html": new_description,
#     }
# }

# put_product(PRODUCT_ID, data)