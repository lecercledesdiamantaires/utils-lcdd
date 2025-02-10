import streamlit as st
import requests
import json
import pandas as pd
import logging
import os
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

# Config Shopify
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
API_VERSION = os.getenv("API_VERSION")
SHOPIFY_STORE = os.getenv("SHOP_URL")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}"
FOLDER_ID = '1KThYIEU4ieN9jZI8N4-tmAUNN8jmDjZs'  # ID du dossier contenant les images

# Configuration logging
logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Interface Streamlit
st.title("Publier des produits sur Shopify depuis un CSV")

uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])

def get_value_or_none(value):
    return value if pd.notna(value) and value != '' else None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())
    
    if st.button("Publier sur Shopify"):
        erreurs = []
        for index, row in df.iterrows():
            if row.get("en_ligne") == "TRUE" or row.get("en_ligne"):
                continue

            product_infos = {}  # Initialiser product_infos avant le bloc try

            try:
                product_infos = {
                    'id': get_value_or_none(row['id']),
                    'title': get_value_or_none(row['titre']), 
                    'product_type': get_value_or_none(row['type_de_produit']),
                    'total_weight_of_jewelry': get_value_or_none(row['poid_total_du_bijoux']),
                    'main_stone': get_value_or_none(row['pierre_principale']),
                    'main_stone_shape': get_value_or_none(row['forme_pierre_principale']),
                    'main_stone_color': get_value_or_none(row['couleur_pierre_principale']),
                    'main_stone_carat': get_value_or_none(row['carat_pierre_principale']),
                    'number_of_stones': get_value_or_none(row['nombre_de_pierres']),
                    'ornamental_stone': get_value_or_none(row['nom_pierre_d_ornements']),
                    'ornamental_stone_color': get_value_or_none(row["couleur_pierre_d_ornements"]),
                    'ornamental_stone_carat': get_value_or_none(row["caratage_pierre_d_ornement"]),
                    'price': get_value_or_none(row['prix']), 
                    'description': get_value_or_none(row['description']),
                    'online': get_value_or_none(row['en_ligne'])
                }
                
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
                        'metafields': metafields,    
                    }     
                }

                product_infos['online'] = 'TRUE'
                product = add_product(data)
                logging.info(f"Product added with ID: {product['product']['id']}")
                product_id = product["product"]["id"]
                collection(product_infos['product_type'], product_id)
                for image in images_url:
                    post_image(product_id, image, product_infos['title'])
                row['en_ligne'] = 'TRUE'
                logging.info(f"Produit ajouté : {product_infos['title']}")
            
            except Exception as e:
                erreurs.append(f"Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
                logging.error(f"Erreur sur {product_infos.get('id', 'inconnu')} : {str(e)}")
        
        if not erreurs:
            st.success("✅ Tous les produits ont été publiés avec succès !")
        else:
            st.error("\n".join(erreurs))