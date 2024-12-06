
def create_options(type):
    colors= {
        "name" : "Couleur de l'or",
        "values" : ["Rose gold","Gold","White gold"]
    }
    carats ={
        "name": "Caratage de l'or",
        "values": ["14", "18"]
    }
    options = []
    if type == 'Bague':
        size = {
            "name" : "Taille",
            "values" : ["48","49","50","51", "52","53", "54","55", "56", "57","58", "59","60","61","62","63"]
        }
        options.append(size)
    elif type == 'Bracelet':
        size = {
            "name" : "Taille",
            "values" : ["XXS","XS","S","M", "L","XL", "XXL"]
        }
        options.append(size)
    options.append(colors)
    options.append(carats)
    return options
