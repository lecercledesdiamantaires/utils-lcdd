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
    print(url)
    response = requests.post(url, json=data)
    print(response.json())
    return response.json()

def post_product(data):
    url = f"{BASE_URL}/admin/api/{API_VERSION}/products.json"
    print(url)
    response = requests.post(url, json=data)
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

response = post_product(data = {
    "product": {
        "title": "Test",
        "body_html": "<p>Test</p>",
        "vendor": "Test",
        "product_type": "bague",
        "tags": "Test",
        "price": "10.00",
        # "variants":[{"option1":"Blue","option2":"155","price":"10.00"},{"option1":"Black","option2":"159"},{"option1":"Blue", "option2":"159"}],"options":[{"name":"Color","values":["Blue","Black"]},{"name":"Size","values":["155","159"]}],
        # "images": [
        #     {
        #         "src": "https://drive.google.com/uc?export=view&id=1DomtgKHQWL2yZG3eKlnE3bVECNQJqc-P"
        #     }
        # ],
        "metafields":[{"namespace":"custom","key":"oui","value":"oui","type":"single_line_text_field"}]
    }
})

print(json.dumps(response, indent=2))

# post_image(14944891633999, data = {
#     "image": {
#         "product_id" : 14944891633999, 
#         "src": "https://drive.google.com/uc?export=view&id=1DomtgKHQWL2yZG3eKlnE3bVECNQJqc-P"
#         }
# })



