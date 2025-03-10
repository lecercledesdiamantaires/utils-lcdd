def create_options(type):
    colors= {
        "name" : "Couleur de l'or",
        "values" : ["Rose gold", "Gold", "White gold"]
    }
    options = []
    if type in ["Baguecatalogue", "Colliercatalogue", "Braceletcatalogue", "Bouclesdoreillescatalogue"]:
        pierres = {
            "name": "Pierre précieuse",
            "values": ["Diamant", "Saphir", "Emeraude", "Rubis"]
        }
        if type == 'Bague Catalogue':
            size = {
                "name" : "Taille",
                "values" : ["48", "50", "52", "54", "56", "58", "60", "62"]
            }
        elif type == 'Collier Catalogue' or type == 'Bracelet Catalogue':
            size = {
                "name" : "Taille",
                "values" : ["XXS","XS","S","M","L","XL","XXL"]
            }
        
        options.append(size)
        options.append(pierres)
    else :
        carats ={
            "name": "Caratage de l'or",
            "values": ["14", "18"]
        }
        options.append(carats)

        if type == 'Bague' or type == 'Alliance':
            size = {
                "name" : "Taille",
                "values" : ["48","49","50","51", "52","53", "54","55", "56", "57","58","59","60","61","62","63"]
            }
            options.append(size)

        elif type == 'Bracelet':
            size = {
                "name" : "Taille",
                "values" : ["XXS","XS","S","M","L","XL","XXL"]
            }
            options.append(size)

    options.append(colors)

    return options
