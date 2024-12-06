import csv;

def get_infos():
    infos = []
    with open(f'./post-product/info-product.csv', 'r', encoding='utf-8') as fichier_csv:
        reader = csv.DictReader(fichier_csv)
        for row in reader:
            product_infos = {
                'id': row['id'],
                'titre': row['titre'],
                'type de produit': row['type_de_produit'],
                'poid total du bijoux': row['poid_total_du_bijoux'],
                'pierre principale': row['pierre_principale'],
                'forme pierre principale': row['forme_pierre_principale'],
                'couleur pierre principale': row['couleur_pierre_principale'],
                'carat pierre principale': row['carat_pierre_principale'],
                'nombre de pierres': row['nombre_de_pierres'],
                'couleur pierre d\'ornements': row['couleur_pierre_d_ornements'],
                'caratage pierre d\'ornement': row['caratage_pierre_d_ornement'],
                'prix': row['prix'],
                'nom produit': row['nom_produit'],
                'description': row['description'],
                'en ligne': row['en_ligne']
            }
            infos.append(product_infos)
    return infos

infos= get_infos()
for info in infos:
    print(info)


