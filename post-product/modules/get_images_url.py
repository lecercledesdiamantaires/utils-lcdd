from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
import logging

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def get_images_url(folder_id, prefix):
    logging.info(f"Fetching images from folder ID: {folder_id} with prefix: {prefix}")
    links = []
    subfolder_id = get_subfolder_id_by_name(folder_id, prefix)

    if subfolder_id:
        logging.info(f"Subfolder ID found: {subfolder_id}")
        links = download_files_in_folder(subfolder_id)
        return links
    else:
        logging.error(f"Subfolder '{prefix}' not found.")
        return None

def get_subfolder_id_by_name(parent_folder_id, subfolder_name):
    logging.info(f"Searching for subfolder '{subfolder_name}' in parent folder ID: {parent_folder_id}")
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    page_token = None

    while True:
        try:
            results = service.files().list(
                q=query,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()
            folders = results.get('files', [])
            logging.debug(f"Found {len(folders)} folders in parent folder ID: {parent_folder_id}")
            for folder in folders:
                if folder['name'] == str(subfolder_name):
                    logging.info(f"Subfolder '{subfolder_name}' found with ID: {folder['id']}")
                    return folder['id']
            page_token = results.get('nextPageToken', None)
            if not page_token:
                break
        except Exception as e:
            logging.error(f"An error occurred while searching for subfolder: {e}")
            break
    logging.warning(f"Subfolder '{subfolder_name}' not found in parent folder ID: {parent_folder_id}")
    return None

def download_files_in_folder(folder_id):
    logging.info(f"Downloading files from folder ID: {folder_id}")
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    files_data = []
    files_data_sorted = []
    links = []

    while True:
        try:
            results = service.files().list(
                q=query,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()
            files = results.get('files', [])
            logging.debug(f"Found {len(files)} files in folder ID: {folder_id}")
            for file in files:  
                download_link = f"https://drive.google.com/uc?id={file['id']}"
                files_data.append((file['name'], download_link))
                response = requests.get(download_link, timeout=30)  # Augmenter le délai d'attente à 30 secondes
                if response.status_code != 200:
                    logging.error(f"Failed to download {file['name']} with status code {response.status_code}")
                else:
                    logging.info(f"Successfully downloaded {file['name']}")

            page_token = results.get('nextPageToken', None)
            if not page_token:
                break
        except requests.exceptions.Timeout as e:
            logging.error(f"Request timed out: {e}")
            break
        except Exception as e:
            logging.error(f"An error occurred while downloading files: {e}")
            break

    # Trier par nom de fichier
    files_data_sorted = sorted(files_data, key=lambda x: x[0])
    logging.debug(f"Sorted files: {files_data_sorted}")

    # Convertir les liens en objets {src: link}
    links = [link for _, link in files_data_sorted]
    logging.info(f"Downloaded {len(links)} files from folder ID: {folder_id}")
    return links

# Exemple d'utilisation
if __name__ == "__main__":
    folder_id = 'your-folder-id'
    prefix = 'your-prefix'
    links = get_images_url(folder_id, prefix)
    logging.info(f"Links: {links}")