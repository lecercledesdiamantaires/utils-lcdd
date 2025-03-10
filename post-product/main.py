import streamlit as st
import requests
import json
import pandas as pd
import logging
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
from google.oauth2.service_account import Credentials


# Config Shopify
API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]
SHOP_NAME = st.secrets["SHOP_NAME"]
API_VERSION = st.secrets["API_VERSION"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"
FOLDER_ID = '1KThYIEU4ieN9jZI8N4-tmAUNN8jmDjZs'  # ID du dossier contenant les images

# Configuration Google Sheets
# GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1EhcVeT6Uh7U_Yv9eoERMJqG-SH2YePKJa8EqWPMde0M/edit?gid=0#gid=0"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/19_V1n8MVrswA-maR5Ic4xGGUdHhQzkXogLvXUUjG7bs/edit?gid=0#gid=0"
SHEET_NAME = "Feuille1"  # Modifier selon ton Google Sheet
# CREDENTIALS_FILE = "./credentials.json"  # Fichier JSON des credentials

service_account_info = json.loads(st.secrets["credentials"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
client = gspread.authorize(creds)

# Configuration logging
logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour récupérer les données du Google Sheet
def get_google_sheet_data(sheet_url, sheet_name):
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    data = sheet.get_all_records()

    # Convertir en DataFrame
    df = pd.DataFrame(data)

    # Supprimer les lignes totalement vides
    df.dropna(how="all", inplace=True)

    # Supprimer les lignes où "en_ligne" est "TRUE"
    if "en_ligne" in df.columns:
        df = df[df["en_ligne"].astype(str).str.upper() != "TRUE"]

    # Supprimer les lignes où "id" est NaN ou non numérique
    df = df[df['id'].apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))]

    # Convertir "id" en entier
    df["id"] = df["id"].astype(int)

    return df


def update_google_sheet(sheet_url, sheet_name, product_id, shopify_id):
    """Met à jour la colonne 'en_ligne' à 'TRUE' pour un produit donné"""
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    cell = sheet.find(str(product_id), in_column=2) 
    if cell:
        sheet.update_cell(cell.row, sheet.find("en_ligne").col, "TRUE")
        sheet.update_cell(cell.row, sheet.find("url").col, f"https://admin.shopify.com/store/cercledesdiamantaires/products/{shopify_id}")


# Interface Streamlit
st.title("Publier les produits")
st.write("ℹ️ Ce script permet de publier les produits sur Shopify à partir du Google Sheet 'info-produit'.")
st.error("Pour la mise en forme du drive :")

st.text(f"""
        1- Respecter les listes de prédéfinies sans les modifier 
        2- Mettre le poids en gramme sans virgule 
        3- Mettre le prix en euro sans virgule 
        4- Les valeurs du caratage sont a mettre avec des points 
        5- Si il y a plusieurs pierres d'ornements il faut mettre toutes les infos dans le meme ordre c'est a dire la première couleur doit correspondre a la couleur de la première pierre qui a été mise et pareil pour le caratage 
        6 - Pour les caratages de pierre d'ornements de plusieurs pierre il faut les séparer avec un tiret comme sur la première ligne exemple
        7 - La valeur de la colonne B doit correspondre au numéro du sous dossier du drive
        """)

if st.button("Charger les données"):
    df = get_google_sheet_data(GOOGLE_SHEET_URL, SHEET_NAME)

    if "Image" in df.columns:
        df = df.drop(columns=["Image"])

    st.session_state["df"] = df 

    st.write("📊 Aperçu du DataFrame chargé :")
    if "df" in st.session_state:
        st.write(st.session_state["df"])



if st.button("Publier sur Shopify"):
    if "df" not in st.session_state:
        st.error("❌ Les données ne sont pas chargées. Cliquez d'abord sur 'Charger les données'.")
    else:
        df = st.session_state["df"]
        st.write("🛍️ Début de la publiation des produits...")

        erreurs = []

        for index, row in df.iterrows():
            if row.get("en_ligne") == "TRUE":
                continue
            try:
                product_infos = {
                    'id': row.get('id'),
                    'title': row.get('titre'), 
                    'product_type': row.get('type_de_produit'),
                    'total_weight_of_jewelry': row.get('poid_total_du_bijoux'),
                    'main_stone': row.get('pierre_principale'),
                    'main_stone_shape': row.get('forme_pierre_principale'),
                    'main_stone_color': row.get('couleur_pierre_principale'),
                    'main_stone_carat': row.get('carat_pierre_principale'),
                    'number_of_stones': row.get('nombre_de_pierres'),
                    'ornamental_stone': row.get('nom_pierre_d_ornements'),
                    'ornamental_stone_color': row.get("couleur_pierre_d_ornements"),
                    'ornamental_stone_carat': row.get("caratage_pierre_d_ornement"),
                    'price': row.get('prix'),
                    'description': row.get('description'),
                    'online': row.get('en_ligne'),
                }
                st.write(f"Produit : {product_infos['title']}, ID : {product_infos['id']}")
                check_product_type(product_infos['id'], product_infos['product_type'])

                description = generate_product_info(
                    product_infos['total_weight_of_jewelry'],
                    product_infos['main_stone'],
                    product_infos['main_stone_carat'],
                    product_infos['ornamental_stone'],
                    product_infos['ornamental_stone_carat'],
                    product_infos['number_of_stones'],
                    product_infos['main_stone_shape'],
                    product_infos['product_type'],
                    product_infos['main_stone_color'],
                    product_infos['ornamental_stone_color'],
                    product_infos['description']
                )

                tags = create_tags(
                    product_infos['product_type'], 
                    product_infos['main_stone'], 
                    product_infos['ornamental_stone']
                )
                images_url = get_images_url(FOLDER_ID, product_infos['id'])
                logging.debug(f"Images URL: {images_url}")
                metafields = get_metafield(
                    product_infos['product_type'],
                    product_infos['main_stone'],
                    product_infos['ornamental_stone'],
                    product_infos['main_stone_color'],
                    product_infos['ornamental_stone_color']
                )
                variants = create_variants(
                    product_infos['price'],
                    product_infos['product_type'],
                    product_infos['total_weight_of_jewelry']
                )
                options = create_options(
                    product_infos['product_type']
                )
                
                data = { 
                    "product" : {
                        'title': title_main(product_infos['title']),
                        'body_html': description,
                        'vendor': 'Le Cercle des Diamantaires',
                        'product_type': product_infos['product_type'],
                        'tags': tags,
                        'variants': variants,
                        'options': options,
                        'metafields': metafields
                    }     
                }
                product = add_product(data)
                logging.info(f"Product added with ID: {product['product']['id']}")
                product_id = product["product"]["id"]
                collection(product_infos['product_type'], product_id)
                st.write("Récupérations des images en cours...")
                for image in images_url:
                    post_image(product_id, image, product_infos['title'])
                logging.info(f"Produit ajouté : {product_infos['title']}")
                st.success(f"✅ Produit ajouté avec succès : https://admin.shopify.com/store/cercledesdiamantaires/products/{product_id}")

                product_infos['online'] = 'TRUE'
                update_google_sheet(GOOGLE_SHEET_URL, SHEET_NAME, product_infos['id'], product_id)


            except Exception as e:
                erreurs.append(f"Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
                logging.error(f"Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
                st.error(f"❌ Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
        if not erreurs:
            st.success("✅ Tous les produits ont été publiés avec succès !")
        else:
            st.error("\n".join(erreurs))