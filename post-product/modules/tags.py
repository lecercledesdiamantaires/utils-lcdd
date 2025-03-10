def create_tags(product_type, primal_stone_name, secondary_stone_name):
    if product_type == 'Baguecatalogue':
        product_type = "bague"
    elif product_type == 'Colliercatalogue':
        product_type = "collier"
    elif product_type == 'Braceletcatalogue':
        product_type = "bracelet"
    elif product_type == 'Boucledoreillescatalogue':
        product_type = "boucle d'oreilles"

    if "-" in secondary_stone_name:
        secondary_stone_name = ", ".join([s.capitalize() for s in secondary_stone_name.split(", ")])
    else:
        secondary_stone_name = secondary_stone_name.capitalize()

    tags = f"{product_type.capitalize()}, {primal_stone_name.capitalize()}, {secondary_stone_name}, Or blanc, Or jaune, Or rose"

    return tags
