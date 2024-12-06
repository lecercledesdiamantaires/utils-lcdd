from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
import json
import base64
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

# Chemin vers votre fichier JSON des informations d'identification
SERVICE_ACCOUNT_FILE = '../credentials.json'
FOLDER_ID = '146Ox-MtR-QPFp3MpJePwboKNY1PbaSdB'  
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authentification avec le compte de service
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Initialiser le client de l'API Drive
service = build('drive', 'v3', credentials=credentials)

# Liste les fichiers dans un dossier spécifique
def list_files_in_folder(folder_id):
    link = []
    # Requête pour lister les fichiers dans un dossier spécifique
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
        print(f'Fichiers dans le dossier {folder_id}:')
        for file in files:
            # Générer le lien du fichier
            download_link = f"https://drive.google.com/uc?id={file['id']}"
            link.append(download_link)

    return link

# Appeler la fonction pour afficher les fichiers du dossier spécifique
IMAGE_URLS = list_files_in_folder(FOLDER_ID)
print(IMAGE_URLS)


# Créer un produit
def create_product(title, description, price, image_urls):
    url = f"https://{API_KEY}:{PASSWORD}@{SHOP_URL}/admin/api/2024-01/products.json"
    
    # Détails du produit
    product_data = {
        "product": {
            "title": title,
            "body_html": description,
            "variants": [{
                "price": price,
                "sku": "SKU001"
            }],
            "images": []  # Utiliser un tableau d'images
        }
    }

    # Ajout d'images via URLs directs
    for img_url in image_urls:
        product_data["product"]["images"].append({
            "product_id" 
            "src": img_url  # Ajouter l'URL de l'image dans le tableau "images"
        })

    # Envoi des données au serveur Shopify
    response = requests.post(url, json=product_data)
    
    if response.status_code == 201:
        print("Produit créé avec succès !")
        print(response.json())  # Affiche les détails du produit pour validation
    else:
        print(f"Erreur {response.status_code}: {response.text}")

# Exemple d'images directes (sans base64)
create_product(
    title="Nom du produit",
    description="Description du produit",
    price="19.99",
    image_urls=IMAGE_URLS  # Utilisez les liens récupérés depuis Google Drive
)
