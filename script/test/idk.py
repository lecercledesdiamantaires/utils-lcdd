import base64
import requests
from io import BytesIO
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE = os.getenv("SHOP_URL")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"


# credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('drive', 'v3', credentials=credentials)

def list_files_in_folder(folder_id):
    link = []
    query = f"'{folder_id}' in parents"
    results = service.files().list(
        q=query,
        pageSize=10,
        fields="nextPageToken, files(id, name)"
    ).execute()

    files = results.get('files', [])

    if not files:
        print(f'Aucun fichier trouvé dans le dossier {folder_id}.')
    else:
        for file in files:
            download_link = f"https://drive.google.com/uc?id={file['id']}"
            link.append(download_link)

    return link

def post_image(product_id, data):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images.json"
    response = requests.post(url, json=data)
    print(response.json())
    return response.json()

def post_product(data):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products.json"
    response = requests.post(url, json=data)
    print(response.raise_for_status())
    return response.json()



# def convert_image_to_base64(image_url):
#     response = requests.get(image_url)
#     if response.status_code == 200:
#         image_data = BytesIO(response.content)
#         base64_data = base64.b64encode(image_data.read()).decode('utf-8')
#         return base64_data
#     else:
#         print(f"Failed to download image. Status code: {response.status_code}")
#         return None

# IMAGE_URLS = list_files_in_folder(FOLDER_ID)
post_product(data = {
    "product": {
    "title": "Bague diamant jaune - Aélia",
    "body_html": "\n    <p>Découvrez notre Bague en Or avec Diamant</p>\n    <div class=\"infos-product\">\n        <h4>Caractéristiques du produit</h4>\n        <!--short-description-->\n        <ul>\n            <li><strong>Poids </strong>: 7.1 grammes</li>\n            <li><strong>Matériau </strong>: Or</li>\n            <li><strong>Pierre principale </strong>: Diamant (1.0 carat)</li>\n            \n    <li><strong>Pierre secondaire</strong> : Diamant, Saphir (1.4 carat)</li>\n    \n            <li><strong>Nombre de pierres </strong>: 18</li>\n            <li><strong>Couleur principale </strong>: Blanc</li>\n            <li><strong>Couleur secondaire </strong>: Blanc, Bleu</li>\n            <li><strong>Forme de la pierre </strong>: Rond</li>\n        </ul>\n        <!--end-short-description-->\n    </div>\n    <br>\n    <p>Photos retouchées</p>\n    ",
    "vendor": "Le Cercle des Diamantaires",
    "product_type": "Bague",
    "tags": "Bague, Diamant, Diamant, saphir, Or blanc, Or jaune, Or rose",
    "images": [
        {
            "src": "https://drive.google.com/uc?id=1X5WqH2jskrbBaPOYKwcRSLaWwjby0Dr4"
        }
    ],
    "variants": [
        {
            "option1": "48",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "48",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "48",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "48",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "48",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "48",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "49",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "49",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "49",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "49",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "49",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "49",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "50",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "50",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "50",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "50",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "50",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "50",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "51",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "51",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "51",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "51",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "51",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "51",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "52",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "52",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "52",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "52",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "52",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "52",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "53",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "53",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "53",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "53",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "53",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "53",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "54",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "54",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "54",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "54",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "54",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "54",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "55",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "55",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "55",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "55",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "55",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "55",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "56",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "56",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "56",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "56",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "56",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "56",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "57",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "57",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "57",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "57",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "57",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "57",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "58",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "58",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "58",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "58",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "58",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "58",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "59",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "59",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "59",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "59",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "59",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "59",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "60",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "60",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "60",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "60",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "60",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "60",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "61",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "61",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "61",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "61",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "61",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "61",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "62",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "62",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "62",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "62",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "62",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "62",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "63",
            "option2": "Rose gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "63",
            "option2": "Rose gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "63",
            "option2": "Gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "63",
            "option2": "Gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "63",
            "option2": "White gold",
            "option3": "14",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "7437.5",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        },
        {
            "option1": "63",
            "option2": "White gold",
            "option3": "18",
            "inventory_policy": "continue",
            "barcode": "",
            "inventory_management": "shopify",
            "price": "8750",
            "weight": 7.1,
            "weight_unit": "g",
            "inventory_quantity": 999,
            "old_inventory_quantity": 999
        }
    ],
    "options": [
        {
            "name": "Taille",
            "values": [
                "48",
                "49",
                "50",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "57",
                "58",
                "59",
                "60",
                "61",
                "62",
                "63"
            ]
        },
        {
            "name": "Couleur de l'or",
            "values": [
                "Rose gold",
                "Gold",
                "White gold"
            ]
        },
        {
            "name": "Caratage de l'or",
            "values": [
                "14",
                "18"
            ]
        }
    ],
    "metafields": [
        {
            "namespace": "custom",
            "key": "pierre_pr_cieuse",
            "value": "[\"gid://shopify/Metaobject/83800850767\",\"gid://shopify/Metaobject/83795837263\"]",
            "type": "list.metaobject_reference"
        },
        {
            "namespace": "custom",
            "key": "couleur_de_la_pierre",
            "value": "[\"gid://shopify/Metaobject/85293171023\",\"gid://shopify/Metaobject/85150695759\"]",
            "type": "list.metaobject_reference"
        },
        {
            "namespace": "custom",
            "key": "couleur_de_l_or",
            "value": "[\"gid://shopify/Metaobject/83803111759\",\"gid://shopify/Metaobject/84184858959\",\"gid://shopify/Metaobject/83803308367\"]",
            "type": "list.metaobject_reference"
        },
        {
            "namespace": "related_products",
            "key": "product_list",
            "value": "[\"gid://shopify/Product/9532796535119\",\"gid://shopify/Product/9462400287055\"]",
            "value_type": "list.product_reference"
        }
    ]
}
}
)
    
#response= post_product(data = {
   
# response = post_product(data = {
#     "product": {
#         "title": "Test",
#         "body_html": "<p>Test</p>",
#         "vendor": "Test",
#         "product_type": "bague",
#         "tags": "Test",
#         "price": "10.00",
#         "variants":[{"option1":"Blue","option2":"155","price":"10.00"},{"option1":"Black","option2":"159"},{"option1":"Blue", "option2":"159"}],"options":[{"name":"Color","values":["Blue","Black"]},{"name":"Size","values":["155","159"]}],
#         "images": [
#             {
#                 "src": "https://drive.google.com/uc?export=view&id=1DomtgKHQWL2yZG3eKlnE3bVECNQJqc-P"
#             }
#         ],
#         "metafields":[{"namespace":"custom", "key":"pierre_pr_cieuse","value": "[\"gid://shopify/Metaobject/83800850767\",\"gid://shopify/Metaobject/83795837263\",\"gid://shopify/Metaobject/83532054863\"]","type":"list.metaobject_reference"
#         }]
#     }
# })

# print(json.dumps(response, indent=2))

# post_image(14944891633999, data = {
#     "image": {
#         "product_id" : 14944891633999, 
#         "src": "https://drive.google.com/uc?export=view&id=1DomtgKHQWL2yZG3eKlnE3bVECNQJqc-P"
#         }
# })



