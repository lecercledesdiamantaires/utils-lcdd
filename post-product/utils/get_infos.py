import csv;

def get_infos():
    infos = []
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
                'ornamental_stone_color': row["couleur_pierre_d_ornements"],
                'ornamental_stone_carat': row["caratage_pierre_d_ornement"],
                'price': row['prix'], 
                'product_name': row['nom_produit'],
                'description': row['description'],
                'online': row['en_ligne']
            }
            infos.append(product_infos)
    return infos




