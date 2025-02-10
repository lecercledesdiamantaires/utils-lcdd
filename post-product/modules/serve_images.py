import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from PIL import Image
from flask import Flask, send_file
from pyngrok import ngrok
import requests

# Variables globales
IMAGE_FOLDER = './images'
CREDS_PATH = './credentials.json'
TOKEN_PATH = './token.json'

# Dossier d'images
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Authentification Google Drive
def authenticate_google_drive():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive.readonly'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, ['https://www.googleapis.com/auth/drive.readonly'])
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

# Télécharger l'image depuis Google Drive
def download_image(drive_service, file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# Convertir l'image en WebP
def convert_image_to_webp(image_data):
    image = Image.open(image_data)
    output = io.BytesIO()
    image.save(output, format="WEBP")
    return output.getvalue()

# Sauvegarder l'image convertie en WebP
def save_image(filename, image_data):
    image_path = os.path.join(IMAGE_FOLDER, filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)
    return image_path

# Serveur Flask pour exposer les images
app = Flask(__name__)

@app.route('/image/<filename>')
def serve_image(filename):
    image_path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/webp')
    else:
        return "Image not found", 404

# Fonction principale pour gérer le téléchargement, la conversion et la mise en ligne
def process_and_upload_images(drive_links):
    # Authentifier avec Google Drive
    drive_service = authenticate_google_drive()

    # Démarrer le tunnel ngrok
    public_url = ngrok.connect(5000)
    print(f" * Ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

    # Liste pour stocker les liens URL générés pour Shopify
    image_urls = []

    for link in drive_links:
        file_id = link.split('/')[-2]  # Récupérer le file_id de l'URL
        image_data = download_image(drive_service, file_id)
        webp_data = convert_image_to_webp(image_data)
        filename = f"{file_id}.webp"
        image_path = save_image(filename, webp_data)

        # Ajouter l'URL publique de l'image à la liste
        image_url = f"{public_url}/image/{filename}"
        image_urls.append(image_url)

    return image_urls