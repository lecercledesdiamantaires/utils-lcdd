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

def update_google_sheet(sheet_url, sheet_name, product_id, shopify_id):
    """Met à jour la colonne 'en_ligne' à 'TRUE' et ajoute l'URL Shopify"""
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    
    try:
        cell = sheet.find(str(product_id), in_column=2)  # Assurez-vous que la colonne 2 contient bien les IDs produits
        if not cell:
            st.error(f"❌ Impossible de trouver le produit {product_id} dans la feuille.")
            return

        headers = sheet.row_values(1)  # Récupère la première ligne contenant les noms des colonnes
        col_en_ligne = headers.index("en_ligne") + 1 if "en_ligne" in headers else None
        col_url = headers.index("url") + 1 if "url" in headers else None

        if col_en_ligne:
            sheet.update_cell(cell.row, col_en_ligne, "TRUE")
        else:
            st.warning("⚠️ Colonne 'en_ligne' non trouvée dans la feuille Google Sheets.")

        if col_url:
            sheet.update_cell(cell.row, col_url, f"https://admin.shopify.com/store/cercledesdiamantaires/products/{shopify_id}")
        else:
            st.warning("⚠️ Colonne 'url' non trouvée dans la feuille Google Sheets.")

    except Exception as e:
        st.error(f"❌ Erreur lors de la mise à jour du Google Sheet : {str(e)}")


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
        produits_traites = 0
        produits_publies = 0
        st.write("🛍️ Début de la publication des produits...")
        progress_bar = st.progress(0)
        
        total_produits = len(df)
        
        for index, row in df.iterrows():
            produits_traites += 1
            progress_bar.progress(produits_traites / total_produits)
            
            if row.get("en_ligne") == "TRUE":
                st.info(f"⏭️ Produit {row.get('id')} déjà en ligne, passage au suivant.")
                continue
                
            try:
                product_infos = {
                    'id': row.get('id'),
                    'title': row.get('titre'), 
                    'product_type': row.get('type_de_produit'),
                    'total_weight_of_jewelry': row.get('poid_total_du_bijoux', 0),  # Accepte une valeur par défaut de 0
                    'main_stone': row.get('pierre_principale'),
                    'main_stone_shape': row.get('forme_pierre_principale'),
                    'main_stone_color': row.get('couleur_pierre_principale'),
                    'main_stone_carat': row.get('carat_pierre_principale', 0),  # Accepte une valeur par défaut de 0
                    'number_of_stones': row.get('nombre_de_pierres'),
                    'ornamental_stone': row.get('nom_pierre_d_ornements'),
                    'ornamental_stone_color': row.get("couleur_pierre_d_ornements"),
                    'ornamental_stone_carat': row.get("caratage_pierre_d_ornement", 0),  # Accepte une valeur par défaut de 0
                    'price': row.get('prix'),
                    'description': row.get('description'),
                    'online': row.get('en_ligne'),
                }
                
                # Vérification des champs obligatoires - poids et caratage exclus des champs obligatoires
                champs_obligatoires = ['id', 'title', 'product_type', 'price', 'main_stone', 'main_stone_shape']
                champs_manquants = [champ for champ in champs_obligatoires if not product_infos.get(champ)]
                
                if champs_manquants:
                    raise ValueError(f"Champs obligatoires manquants: {', '.join(champs_manquants)}")
                
                # Vérification et correction des valeurs numériques nulles ou vides
                if product_infos['total_weight_of_jewelry'] is None or product_infos['total_weight_of_jewelry'] == '':
                    product_infos['total_weight_of_jewelry'] = 0
                    st.info(f"ℹ️ Produit {product_infos['id']}: Poids total définit à 0 par défaut")
                    
                if product_infos['main_stone_carat'] is None or product_infos['main_stone_carat'] == '':
                    product_infos['main_stone_carat'] = 0
                    st.info(f"ℹ️ Produit {product_infos['id']}: Caratage pierre principale définit à 0 par défaut")
                
                if product_infos['ornamental_stone_carat'] is None or product_infos['ornamental_stone_carat'] == '':
                    product_infos['ornamental_stone_carat'] = 0
                    
                st.write(f"Produit : {product_infos['title']}, ID : {product_infos['id']}")
                
                try:
                    check_product_type(product_infos['id'], product_infos['product_type'])
                except Exception as e:
                    raise ValueError(f"Type de produit invalide: {str(e)}")

                try:
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
                except Exception as e:
                    raise ValueError(f"Erreur lors de la génération de la description: {str(e)}")

                try:
                    tags = create_tags(
                        product_infos['product_type'], 
                        product_infos['main_stone'], 
                        product_infos['ornamental_stone']
                    )
                except Exception as e:
                    raise ValueError(f"Erreur lors de la création des tags: {str(e)}")
                
                try:
                    images_url = get_images_url(FOLDER_ID, product_infos['id'])
                    if not images_url:
                        st.warning(f"⚠️ Aucune image trouvée pour le produit {product_infos['id']}.")
                    logging.debug(f"Images URL: {images_url}")
                except Exception as e:
                    raise ValueError(f"Erreur lors de la récupération des images: {str(e)}")
                
                try:
                    metafields = get_metafield(
                        product_infos['product_type'],
                        product_infos['main_stone'],
                        product_infos['ornamental_stone'],
                        product_infos['main_stone_color'],
                        product_infos['ornamental_stone_color']
                    )
                except Exception as e:
                    raise ValueError(f"Erreur lors de la création des métadonnées: {str(e)}")
                
                try:
                    variants = create_variants(
                        product_infos['price'],
                        product_infos['product_type'],
                        product_infos['total_weight_of_jewelry']
                    )
                except Exception as e:
                    raise ValueError(f"Erreur lors de la création des variantes: {str(e)}")
                
                try:
                    options = create_options(
                        product_infos['product_type']
                    )
                except Exception as e:
                    raise ValueError(f"Erreur lors de la création des options: {str(e)}")
                
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
                
                try:
                    product = add_product(data)
                    logging.info(f"Product added with ID: {product['product']['id']}")
                    product_id = product["product"]["id"]
                except Exception as e:
                    raise ValueError(f"Erreur lors de l'ajout du produit sur Shopify: {str(e)}")
                
                try:
                    collection(product_infos['product_type'], product_id)
                except Exception as e:
                    st.warning(f"⚠️ Produit créé mais erreur lors de l'ajout à la collection: {str(e)}")
                
                st.write("Récupération des images en cours...")
                images_ajoutees = 0
                for image in images_url:
                    try:
                        # Vérifie que l'URL de l'image n'est pas vide
                        if not image:
                            raise ValueError("L'URL de l'image est vide ou nulle")
                            
                        post_image(product_id, image, product_infos['title'])
                        images_ajoutees += 1
                    except ValueError as e:
                        st.warning(f"⚠️ {str(e)} pour le produit {product_infos['id']}")
                    except Exception as e:
                        st.warning(f"⚠️ Erreur lors de l'ajout de l'image {image}: {str(e)}")
                
                if len(images_url) > 0 and images_ajoutees == 0:
                    st.error(f"❌ Aucune image n'a pu être ajoutée pour le produit {product_infos['id']}")
                elif images_ajoutees < len(images_url):
                    st.warning(f"⚠️ Seulement {images_ajoutees}/{len(images_url)} images ont été ajoutées.")
                
                logging.info(f"Produit ajouté : {product_infos['title']}")
                st.success(f"✅ Produit ajouté avec succès : https://admin.shopify.com/store/cercledesdiamantaires/products/{product_id}")

                try:
                    product_infos['online'] = 'TRUE'
                    update_google_sheet(GOOGLE_SHEET_URL, selected_sheet, product_infos['id'], product_id)
                except Exception as e:
                    st.warning(f"⚠️ Produit créé mais erreur lors de la mise à jour de la feuille Google: {str(e)}")
                
                produits_publies += 1
                
            except ValueError as e:
                erreurs.append(f"Erreur sur {row.get('id', 'inconnu')} : {str(e)}")
                st.error(f"❌ Erreur sur {row.get('id', 'inconnu')} : {str(e)}")
            except Exception as e:
                erreurs.append(f"Erreur inattendue sur {row.get('id', 'inconnu')} : {str(e)}")
                st.error(f"❌ Erreur inattendue sur {row.get('id', 'inconnu')} : {str(e)}")
        
        if not erreurs:
            st.success(f"✅ Tous les produits ({produits_publies}/{total_produits}) ont été publiés avec succès !")
        else:
            st.warning(f"⚠️ {produits_publies}/{total_produits} produits publiés. {len(erreurs)} erreurs rencontrées.")
            with st.expander("Détails des erreurs"):
                for erreur in erreurs:
                    st.error(erreur)