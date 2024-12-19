import os
import requests
import unicodedata
from PIL import Image
from io import BytesIO
import time
import json
from dotenv import load_dotenv
import shutil

load_dotenv()

LIMIT = 250  
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
FALSE_URL = "https://cercledesdiamantaires.myshopify.com/admin/api/2024-01/products.json"
SHOPIFY_STORE = os.getenv("SHOP_URL")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"

def clean_title(product_title):
    product_title = product_title.replace("- ", "")
    product_title = product_title.replace(" ", "_")
    product_title = "".join(c if c.isalnum() or c in ("-", "_") else "" for c in product_title)
    nfkd_form = unicodedata.normalize('NFKD', product_title)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_all_products():
    products = []
    next_page_url = f"{BASE_URL}/admin/api/{API_VERSION}/products.json?limit={LIMIT}"

    while next_page_url:
        response = requests.get(next_page_url)
        response.raise_for_status()  # Vérifie s'il y a une erreur HTTP
        data = response.json()
        products.extend(data["products"])
        print(len(products))
        if "Link" in response.headers:
            links = response.headers["Link"]
            if 'rel="next"' in links:
                next_page_url = links.split(",")[0].split(";")[0].strip("<>")
                
                if FALSE_URL and FALSE_URL in next_page_url:
                    next_page_url = next_page_url.replace(FALSE_URL, f"{BASE_URL}/admin/api/{API_VERSION}/products.json")
            else:
                next_page_url = None
        else:
            next_page_url = None
        

    return products


def get_images(product_id):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    images = []
    for img in data.get('images', []):
        images.append({
            "id" : img.get("id"),
            "src": img.get("src"),
            "alt": img.get("alt", "")
        })

    print(" --- ")
    print(f"Images récupérées pour le produit {product_id}: {len(images)}")
    print(" --- ")

    return images


def delete_image(product_id, image_id) :
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images/{image_id}.json"
    response = requests.delete(url)
    response.raise_for_status()


def convert_to_webp(image_data, output_dir, image_name, product_title):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Supprimer le dossier
    os.makedirs(output_dir, exist_ok=True)  # Recréer le dossier vide
    image = Image.open(image_data)
    output_path = os.path.join(output_dir, f"{product_title}.webp")
    image.save(output_path, format="WEBP")
    return output_path


def post_image(product_id, src, alt, retries=5, delay=8):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images.json"
    data = {"image": {"src": src, "alt": alt}}
    for attempt in range(retries):
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Tentative {attempt + 1} échouée: {e}")
            if attempt < retries - 1:
                time.sleep(delay)

    print("Échec après toutes les tentatives.")
    return None


def process_all_images():
    products = get_all_products()
    output_dir = "./script/test_images"
    os.makedirs(output_dir, exist_ok=True)

    for product in products:
        product_id = product.get('id')

        product_title = product.get('title')
        product_title = clean_title(product_title)
        if not product_id:
            continue

        images = get_images(product_id)
        for img_data in images:
            try:
                response = requests.get(img_data['src'])
                response.raise_for_status()

                converted_image_path = convert_to_webp(BytesIO(response.content), output_dir, os.path.basename(img_data['src']), product_title)

                ngrok_url = "https://43b9-2a01-cb04-31a-7300-d5c3-dbe0-1132-3a6.ngrok-free.app"  
                src_url = f"{ngrok_url}/{os.path.basename(converted_image_path)}"
                if post_image(product_id, src_url, product_title) :
                    delete_image(product_id, img_data['id'])
                    print('IMAGE DELETE')



            except Exception as e:
                print(f"Erreur lors du traitement de l'image : {e}")


process_all_images()
