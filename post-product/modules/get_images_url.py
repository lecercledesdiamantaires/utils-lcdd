from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import requests
import logging
from io import BytesIO
from PIL import Image

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

ARCHIVE_FOLDER_NAME = "Archive"

def get_images_url(folder_id, prefix):
    logging.info(f"Fetching images from folder ID: {folder_id} with prefix: {prefix}")
    links = []
    subfolder_id = get_subfolder_id_by_name(folder_id, prefix)
    
    if subfolder_id:
        logging.info(f"Subfolder ID found: {subfolder_id}")
        archive_folder_id = get_or_create_subfolder(folder_id, ARCHIVE_FOLDER_NAME)
        logging.info(f"Archive folder ID: {archive_folder_id}")
        links = process_images_in_folder(subfolder_id, archive_folder_id)
        return links
    else:
        logging.error(f"Subfolder '{prefix}' not found.")
        return None

def get_subfolder_id_by_name(parent_folder_id, subfolder_name):
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    page_token = None
    
    while True:
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)", pageToken=page_token).execute()
        for folder in results.get('files', []):
            if folder['name'] == str(subfolder_name):
                return folder['id']
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    
    return None

def get_or_create_subfolder(parent_folder_id, subfolder_name):
    subfolder_id = get_subfolder_id_by_name(parent_folder_id, subfolder_name)
    if subfolder_id:
        return subfolder_id
    
    file_metadata = {
        'name': subfolder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    logging.info(f"Created subfolder '{subfolder_name}' with ID: {folder.get('id')}")
    return folder.get('id')

def process_images_in_folder(folder_id, archive_folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    links = []
    for file in files:
        if file['name'].lower().endswith('.webp'):
            logging.info(f"Skipping already WebP image: {file['name']}")
            links.append(f"https://drive.google.com/uc?id={file['id']}")
            continue

        image_data = download_image(file['id'])
        if image_data:
            webp_image = convert_to_webp(image_data)
            webp_file_id = upload_image_to_drive(webp_image, f"{file['name'].rsplit('.', 1)[0]}.webp", folder_id)
            if webp_file_id:
                links.append(f"https://drive.google.com/uc?id={webp_file_id}")
                move_original_file(file['id'], archive_folder_id)
    return links

def download_image(file_id):
    try:
        request = service.files().get_media(fileId=file_id)
        image_data = BytesIO(request.execute())
        return image_data
    except Exception as e:
        logging.error(f"Error downloading image {file_id}: {e}")
        return None

def convert_to_webp(image_data):
    try:
        image = Image.open(image_data)
        webp_buffer = BytesIO()
        image.save(webp_buffer, format="WEBP", quality=80)
        webp_buffer.seek(0)
        return webp_buffer
    except Exception as e:
        logging.error(f"Error converting image to WebP: {e}")
        return None

def upload_image_to_drive(image_data, filename, folder_id):
    try:
        file_metadata = {'name': filename, 'parents': [folder_id]}
        media = MediaIoBaseUpload(image_data, mimetype='image/webp', resumable=True)
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return uploaded_file.get('id')
    except Exception as e:
        logging.error(f"Error uploading WebP image: {e}")
        return None

def move_original_file(file_id, archive_folder_id):
    try:
        # Récupérer les informations du fichier pour obtenir son dossier parent actuel
        file = service.files().get(fileId=file_id, fields="parents").execute()
        current_parents = ",".join(file.get("parents", []))  # Convertir la liste en string

        # Déplacer le fichier vers le dossier d'archive
        service.files().update(
            fileId=file_id,
            addParents=archive_folder_id,
            removeParents=current_parents,  # Utilisation correcte du parent actuel
            fields="id"
        ).execute()

        logging.info(f"Successfully moved original file {file_id} to archive folder {archive_folder_id}")

    except Exception as e:
        logging.error(f"Error moving original file {file_id} to archive folder {archive_folder_id}: {e}")
