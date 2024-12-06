import os
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials




load_dotenv()

SHOPIFY_API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("DATABASE_URL")
SHOPIFU_API_PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
LIMIT = os.getenv("LIMIT")
FALSE_URL = os.getenv("FALSE_URL")
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE")


SERVICE_ACCOUNT_FILE = '../credentials.json'

SCOPES = ['https://www.googleapis.com/auth/drive']

# Authentification avec le compte de service
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Initialiser le client de l'API Drive
service = build('drive', 'v3', credentials=credentials)

# Liste les fichiers dans le Drive
def list_files():
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('Aucun fichier trouvé.')
    else:
        print('Fichiers:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

# Appeler la fonction pour afficher les fichiers
list_files()
