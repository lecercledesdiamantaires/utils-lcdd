import streamlit as st
import json
import pandas as pd
import logging
import gspread
import re
from google.oauth2.service_account import Credentials
from modules.options import create_options
from modules.check_product_type import check_product_type
from modules.tags import create_tags
from modules.description import generate_product_info
from modules.title import title_main
from modules.get_images_url import get_images_url
from modules.variants import create_variants
from modules.metafields import get_metafield
from modules.add_product import add_product
from modules.post_image import post_image
from modules.collection import collection

# Valeurs par défaut
DEFAULT_FOLDER_URL = "https://drive.google.com/drive/folders/1KThYIEU4ieN9jZI8N4-tmAUNN8jmDjZs"
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1EhcVeT6Uh7U_Yv9eoERMJqG-SH2YePKJa8EqWPMde0M/edit?gid=0#gid=0"

# Interface Streamlit
st.title("Publier les produits sur Shopify")
st.write("ℹ️ Ce script permet de publier les produits sur Shopify à partir d'un Google Sheet.")

# Fonction pour extraire l'ID d'un dossier Google Drive
def extract_folder_id(folder_url):
    match = re.search(r"folders/([a-zA-Z0-9_-]+)", folder_url)
    return match.group(1) if match else None

# Entrées utilisateur pour le dossier Drive et la feuille Google Sheets
FOLDER_URL = st.text_input("URL du dossier Google Drive contenant les images :", DEFAULT_FOLDER_URL)
FOLDER_ID = extract_folder_id(FOLDER_URL) if FOLDER_URL else ""
GOOGLE_SHEET_URL = st.text_input("URL du Google Sheet contenant les produits :", DEFAULT_GOOGLE_SHEET_URL)

# Connexion Google Sheets
service_account_info = json.loads(st.secrets["credentials"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
client = gspread.authorize(creds)

# Fonction pour récupérer les noms des feuilles d'un Google Sheet
def get_sheet_names(sheet_url):
    sheet = client.open_by_url(sheet_url)
    return sheet.worksheets()

# Récupérer les noms des feuilles
sheets = get_sheet_names(GOOGLE_SHEET_URL)
sheet_names = [sheet.title for sheet in sheets]
selected_sheet = st.selectbox("Sélectionnez une feuille :", sheet_names, index=0)

# Fonction pour récupérer les données du Google Sheet
def get_google_sheet_data(sheet_url, sheet_name):
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    df = pd.DataFrame(sheet.get_all_records())
    df.dropna(how="all", inplace=True)
    if "en_ligne" in df.columns:
        df = df[df["en_ligne"].astype(str).str.upper() != "TRUE"]
    df = df[df['id'].apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))]
    df["id"] = df["id"].astype(int)
    return df

# Charger les données
df = None
if st.button("Charger les données"):
    df = get_google_sheet_data(GOOGLE_SHEET_URL, selected_sheet)
    st.session_state["df"] = df
    st.write("📊 Aperçu du DataFrame chargé :", df)

# Publier les produits sur Shopify
if st.button("Publier sur Shopify"):
    if "df" not in st.session_state:
        st.error("❌ Les données ne sont pas chargées. Cliquez d'abord sur 'Charger les données'.")
    else:
        df = st.session_state["df"]
        erreurs = []
        st.write("🛍️ Début de la publication des produits...")
        for _, row in df.iterrows():
            if row.get("en_ligne") == "TRUE":
                continue
            try:
                product_infos = {key: row.get(key) for key in row.keys()}
                description = generate_product_info(
                    product_infos['poid_total_du_bijoux'],
                    product_infos['pierre_principale'],
                    product_infos['carat_pierre_principale'],
                    product_infos['nom_pierre_d_ornements'],
                    product_infos['caratage_pierre_d_ornement'],
                    product_infos['nombre_de_pierres'],
                    product_infos['forme_pierre_principale'],
                    product_infos['type_de_produit'],
                    product_infos['couleur_pierre_principale'],
                    product_infos['couleur_pierre_d_ornements'],
                    product_infos['description']
                )
                images_url = get_images_url(FOLDER_ID, product_infos['id'])
                data = {
                    "product": {
                        'title': title_main(product_infos['titre']),
                        'body_html': description,
                        'vendor': 'Le Cercle des Diamantaires',
                        'product_type': product_infos['type_de_produit'],
                        'tags': create_tags(product_infos['type_de_produit'], product_infos['pierre_principale'], product_infos['nom_pierre_d_ornements']),
                        'variants': create_variants(product_infos['prix'], product_infos['type_de_produit'], product_infos['poid_total_du_bijoux']),
                        'options': create_options(product_infos['type_de_produit']),
                        'metafields': get_metafield(product_infos['type_de_produit'], product_infos['pierre_principale'], product_infos['nom_pierre_d_ornements'], product_infos['couleur_pierre_principale'], product_infos['couleur_pierre_d_ornements'])
                    }
                }
                product = add_product(data)
                product_id = product["product"]["id"]
                collection(product_infos['type_de_produit'], product_id)
                for image in images_url:
                    post_image(product_id, image, product_infos['titre'])
                st.success(f"✅ Produit ajouté : https://admin.shopify.com/store/cercledesdiamantaires/products/{product_id}")
            except Exception as e:
                erreurs.append(f"Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
                st.error(f"❌ Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
        if not erreurs:
            st.success("✅ Tous les produits ont été publiés avec succès !")
        else:
            st.error("\n".join(erreurs))
