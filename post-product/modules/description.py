import logging

logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def check_first_paragraph(first_paragraph, product_type, primal_stone_name):
    if product_type in ["Baguecatalogue", "Colliercatalogue", "Braceletcatalogue", "Boucledoreillescatalogue"]:
        primal_stone_name = "la pierre principale de votre choix, sertie sur une monture en Or de la couleur de votre choix. Si les options proposées ne vous conviennent pas, remplissez le formulaire de personnalisation pour découvrir des possibilités infinit."

    if product_type == 'Baguecatalogue':
        product_type = "bague"
    elif product_type == 'Colliercatalogue':
        product_type = "collier"
    elif product_type == 'Braceletcatalogue':
        product_type = "bracelet"
    elif product_type == 'Boucledoreillescatalogue':
        product_type = "boucle d'oreille"
    

    if not first_paragraph:
        return f"<p>Découvrez notre {product_type} en Or avec {primal_stone_name}</p>"
    else:
        return f"<p>{first_paragraph}</p>"


def convert_to_float(value):
    if isinstance(value, (int, float)):
        logging.info(f"{value} est déjà un nombre")
        return value
    try:
        value = value.replace(',', '.')
        value = value.replace(' ', '')
        return float(value)
    except ValueError as e:
        logging.error(f"Erreur de conversion de {value}: {e}")
        raise ValueError(f"Erreur de conversion de {value}: {e}")

def check_secondary_stones(secondary_stone_name, secondary_stone_carat):
    stones = []
    if secondary_stone_name and secondary_stone_carat:
        if ", " in secondary_stone_name:
            names = secondary_stone_name.split(", ")
            carats = secondary_stone_carat.split("-")
            for name, carat in zip(names, carats):
                carat = convert_to_float(carat)
                stones.append({"name": name, "carat": carat})
        else:
            stones.append({
                "name": secondary_stone_name,
                "carat": convert_to_float(secondary_stone_carat)
            })
    return stones

def write_secondary_stones(secondary_stones):
    def format_stone(stone):
        carat_unit = "carat" if stone['carat'] < 2 else "carats"
        return f"{stone['name']} ({stone['carat']} {carat_unit})"

    if not secondary_stones:
        return ""
    
    title = "<strong>Pierres secondaires</strong>" if len(secondary_stones) > 1 else "<strong>Pierre secondaire</strong>"
    formatted_stones = ", ".join(format_stone(stone) for stone in secondary_stones)

    return f"<li>{title} : {formatted_stones}</li>"

def generate_product_info(weight, primal_stone_name, carat_primal_stone, secondary_stone_name, 
                          carat_secondary_stone, stone_number, stone_shape, product_type, 
                          main_color, secondary_color, first_paragraph=None):
    weight = convert_to_float(weight)
    carat_primal_stone = convert_to_float(carat_primal_stone)
    first_paragraph = check_first_paragraph(first_paragraph, product_type, primal_stone_name)
    secondary_stones = check_secondary_stones(secondary_stone_name, carat_secondary_stone)
    
    product_info = {
        "weight": weight,
        "primal_stone": {"name": primal_stone_name, "carat": carat_primal_stone, "color": main_color},
        "secondary_stones": secondary_stones,
        "stone_number": stone_number,
        "stone_shape": stone_shape,
        "main_color": main_color,
        "secondary_color": secondary_color
    }
    return write_description(product_info, first_paragraph, product_type)

def write_description(product_info, first_paragraph, product_type):
    if product_type in ["Baguecatalogue", "Colliercatalogue", "Braceletcatalogue", "Bouclesdoreillescatalogue"]:
        description = f"""
        {first_paragraph}
        <div class="infos-product">
            <h4>Caractéristiques du produit</h4>
            <ul>
                <li><strong>Poids</strong>: Le poids dépends des options que vous choisirez. </li>
                <li><strong>Matériau</strong>: Or de votre choix</li>
                <li><strong>Pierre principale</strong>: Pierre principale au choix ({product_info['primal_stone']['carat']} {"carat" if product_info['primal_stone']['carat'] < 2 else "carats"})</li>
                <li><strong>Couleur principale</strong>: Au choix</li>
                {write_secondary_stones(product_info['secondary_stones'])}
                {f"<li><strong>Nombre de pierres</strong>: {product_info['stone_number']}</li>" if product_info.get('stone_number') else ""}
                {f"<li><strong>Couleur secondaire</strong>: {product_info['secondary_color']}</li>" if product_info.get('secondary_color') else ""}
                {f"<li><strong>Forme de la pierre</strong>: {product_info['stone_shape']}</li>" if product_info.get('stone_shape') else ""}
            </ul>
        </div>
        <br>
        <p>Photos retouchées</p>
        """

    else :
        description = f"""
        {first_paragraph}
        <div class="infos-product">
            <h4>Caractéristiques du produit</h4>
            <ul>
                <li><strong>Poids</strong>: {product_info['weight']} {"gramme" if product_info['weight'] < 2 else "grammes"}</li>
                <li><strong>Matériau</strong>: Or</li>
                <li><strong>Pierre principale</strong>: {product_info['primal_stone']['name']} ({product_info['primal_stone']['carat']} {"carat" if product_info['primal_stone']['carat'] < 2 else "carats"})</li>
                <li><strong>Couleur principale</strong>: {product_info['main_color']}</li>
                {write_secondary_stones(product_info['secondary_stones'])}
                {f"<li><strong>Nombre de pierres</strong>: {product_info['stone_number']}</li>" if product_info.get('stone_number') else ""}
                {f"<li><strong>Couleur secondaire</strong>: {product_info['secondary_color']}</li>" if product_info.get('secondary_color') else ""}
                {f"<li><strong>Forme de la pierre</strong>: {product_info['stone_shape']}</li>" if product_info.get('stone_shape') else ""}
            </ul>
        </div>
        <br>
        <p>Photos retouchées</p>
        """
    return description
