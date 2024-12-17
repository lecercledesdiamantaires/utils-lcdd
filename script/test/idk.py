import base64
import requests
from io import BytesIO
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
import json
import base64
import os
import time
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

def post_image_with_retry(product_id, src, retries=5, delay=5):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products/{product_id}/images.json"
    data = {
        "image": {
            src
        }
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            print(f"Image posted successfully: {data['image']['src']}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Failed to post image.")
                return None

# Utilisation de la fonction avec réessai
post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1O9yb6Cmijp5KqsJWMWalkzvbWo7BdAZe"
    }
})

post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1IqDGXGnSdrLRJo4kD8TQ775eX816Meo2"
    }
})

post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1ExEunQ4WFN_dXdYVwPh2JaOe5EPVb5-X"
    }
})
post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1O9yb6Cmijp5KqsJWMWalkzvbWo7BdAZe"
    }
})

post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1IqDGXGnSdrLRJo4kD8TQ775eX816Meo2"
    }
})

post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1ExEunQ4WFN_dXdYVwPh2JaOe5EPVb5-X"
    }
})
post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1IqDGXGnSdrLRJo4kD8TQ775eX816Meo2"
    }
})

post_image_with_retry(15018965500239, data={
    "image": {
        "src": "https://drive.google.com/uc?id=1ExEunQ4WFN_dXdYVwPh2JaOe5EPVb5-X"
    }
})

# post_image(15018965500239, data = {
#     "image" : 
#         {
#             "src" : "https://drive.google.com/uc?id=1O9yb6Cmijp5KqsJWMWalkzvbWo7BdAZe"
#         }
# })

# post_image(15018965500239, data = {
#     "image" : 
#         {
#             "src" : "https://drive.google.com/uc?id=1IqDGXGnSdrLRJo4kD8TQ775eX816Meo2" 
#         }
# })
# post_image(15018965500239, data = {
#     "image" : 
#         {
#             "src" : "https://drive.google.com/uc?id=1ExEunQ4WFN_dXdYVwPh2JaOe5EPVb5-X"
#         }
# })
# post_image(15018965500239, data = {
#     "image" : 
#         {
#             "src" : "https://drive.google.com/uc?id=1whiMTj_fNIk6z5iHrKPrO9z6rnwb4U_E"
#         }
# })


# IMAGE_URLS = list_files_in_folder(FOLDER_ID)
# post_product(data = {
#     "product": {
#         "title": "Bague diamant jaune - Aélia",
#         "body_html": "\n    <p>Découvrez notre Collier en Or avec Diamant</p>\n    <div class=\"infos-product\">\n        <h4>Caractéristiques du produit</h4>\n        <!--short-description-->\n        <ul>\n            <li><strong>Poids </strong>: 7.1 grammes</li>\n            <li><strong>Matériau </strong>: Or</li>\n            <li><strong>Pierre principale </strong>: Diamant (1.0 carats)</li>\n            \n    <li>Pierre secondaire : Diamant, Saphir (1.4 carats)</li>\n    \n            <li><strong>Nombre de pierres </strong>: 18</li>\n            <li><strong>Couleur principale </strong>: Blanc, Bleu</li>\n            <li><strong>Couleur secondaire </strong>: </li>\n            <li><strong>Forme de la pierre </strong>: Rond</li>\n        </ul>\n        <!--end-short-description-->\n    </div>\n    <br>\n    <p>Photos retouchées</p>\n    ",
#         "vendor": "Le Cercle des Diamantaires",
#         "product_type": "Collier",
#         "tags": "Collier, Diamant, Diamant, saphir, Or blanc, Or jaune, Or rose.",
#         "images": [
#             {
#                 "src": "https://drive.google.com/uc?id=1X5WqH2jskrbBaPOYKwcRSLaWwjby0Dr4"
#             }
#         ],
#         "variants": [
#             {
#                 "option1": "Rose gold",
#                 "option2": "14",
#                 "price": "7437.5",
#                 "weight": "7,1",
#                 "inventory_quantity": 999,
#                 "old_inventory_quantity": 999
#             },
#             {
#                 "option1": "Rose gold",
#                 "option2": "18",
#                 "price": "8750",
#                 "weight": "7,1",
#                 "inventory_quantity": 999,
#                 "old_inventory_quantity": 999
#             },
#             {
#                 "option1": "Gold",
#                 "option2": "14",
#                 "price": "7437.5",
#                 "weight": "7,1",
#                 "inventory_quantity": 999,
#                 "old_inventory_quantity": 999
#             },
#             {
#                 "option1": "Gold",
#                 "option2": "18",
#                 "price": "8750",
#                 "weight": "7,1",
#                 "inventory_quantity": 999,
#                 "old_inventory_quantity": 999
#             },
#             {
#                 "option1": "White gold",
#                 "option2": "14",
#                 "price": "7437.5",
#                 "weight": "7,1",
#                 "inventory_quantity": 999,
#                 "old_inventory_quantity": 999
#             },
#             {
#                 "option1": "White gold",
#                 "option2": "18",
#                 "price": "8750",
#                 "weight": "7,1",
#                 "inventory_quantity": 999,
#                 "old_inventory_quantity": 999
#             }
#         ],
#         "options": [
#             {
#                 "name": "Couleur de l'or",
#                 "values": [
#                     "Rose gold",
#                     "Gold",
#                     "White gold"
#                 ]
#             },
#             {
#                 "name": "Caratage de l'or",
#                 "values": [
#                     "14",
#                     "18"
#                 ]
#             }
#         ],
#         "metafields": [
#             {
#                 "namespace": "custom",
#                 "key": "pierre_pr_cieuse",
#                 "value": "[\"gid://shopify/Metaobject/83800850767\",\"gid://shopify/Metaobject/83795837263\"]",
#                 "type": "list.metaobject_reference"
#             },
#             {
#                 "namespace": "custom",
#                 "key": "couleur_de_la_pierre",
#                 "value": "[\"gid://shopify/Metaobject/85293171023\",\"gid://shopify/Metaobject/85150695759\"]",
#                 "type": "list.metaobject_reference"
#             },
#             {
#                 "namespace": "custom",
#                 "key": "couleur_de_l_or",
#                 "value": "[\"gid://shopify/Metaobject/83803111759\",\"gid://shopify/Metaobject/84184858959\",\"gid://shopify/Metaobject/83803308367\"]",
#                 "type": "list.metaobject_reference"
#             },
#             {
#                 "namespace": "related_products",
#                 "key": "product_list",
#                 "value": "[\"gid://shopify/Product/9473876427087\",\"gid://shopify/Product/9472268468559\"]",
#                 "value_type": "list.product_reference"
#             }
#         ]
#     }
# }
# )
    
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



