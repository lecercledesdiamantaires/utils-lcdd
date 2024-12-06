from get_infos import get_infos

colors= {
    "name" : "Couleur de l'or",
    "values" : ["Rose gold","Gold","White gold"]
}

carats ={
    "name": "Caratage de l'or",
    "values": ["14", "18"]
}


def create_options(colors, carats):
    infos = get_infos()
    options = []
    for info in infos:
        if info['product_type'] == 'Bague':
            size = {
                "name" : "Taille",
                "values" : ["48","49","50","51", "52","53", "54","55", "56", "57","58", "59","60","61","62","63"]
            }
            options.append(size)
        elif info['product_type'] == 'Bracelet':
            size = {
                "name" : "Taille",
                "values" : ["XXS","XS","S","M", "L","XL", "XXL"]
            }
            options.append(size)
        options.append(colors)
        options.append(carats)
    return options

        
create_options(colors, carats)