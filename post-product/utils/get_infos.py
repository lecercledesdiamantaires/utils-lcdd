import csv;
from options import create_options
from check_product_type import check_product_type
from tags import tags
from description import main as description_main
from title import main as title_main
from check_product_type import check_product_type
from price import get_price 
from get_images_url import get_images_url
from variants import create_variants
from metafield import get_metafield

FOLDER_ID = '1TE90qtOXN1qqaPpNPyf81aTeJvVd9Zm3'  # ID du dossier contenant les images

def get_infos():
    with open(f'./post-product/info-product.csv', 'r', encoding='utf-8') as fichier_csv:
        reader = csv.DictReader(fichier_csv)
        for row in reader:
            product_infos = {
                'id': row['id'],
                'title': row['titre'], 
                'product_type': row['type_de_produit'],
                'total_weight_of_jewelry': row['poid_total_du_bijoux'],
                'main_stone': row['pierre_principale'],
                'main_stone_shape': row['forme_pierre_principale'],
                'main_stone_color': row['couleur_pierre_principale'],
                'main_stone_carat': row['carat_pierre_principale'],
                'number_of_stones': row['nombre_de_pierres'],
                'ornamental_stone': row['nom_pierre_d_ornements'],
                'ornamental_stone_color': row["couleur_pierre_d_ornements"],
                'ornamental_stone_carat': row["caratage_pierre_d_ornement"],
                'price': row['prix'], 
                'product_name': row['nom_produit'],
                'description': row['description'],
                'online': row['en_ligne']
            }
            check_product_type(product_infos['product_type'])
            description = description_main(
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
            tags = tags(
                product_infos['product_type'], 
                product_infos['main_stone'], 
                product_infos['ornamental_stone']
                )
            images_url = get_images_url(FOLDER_ID, product_infos['id'])
            metafields = get_metafield(
                product_infos['product_type'],
                product_infos['main_stone'],
                product_infos['ornamental_stone'],
                product_infos['main_stone_color'],
                product_infos['ornamental_stone_color']
                )
            data = {
                'id' : product_infos['id'],
                'title': title_main(product_infos['title']),
                'body_html': description,
                'vendor': 'Le Cercle des Diamantaires',
                'product_type': product_infos['product_type'],
                'tags': tags,
                'images': images_url,
                
                'metafileds': metafields,

            }





