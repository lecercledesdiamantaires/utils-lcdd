
def check_first_paragraph(first_paragraph, product_type, primal_stone_name):
    if not first_paragraph:
        return f"<p>Découvrez notre {product_type} en Or avec {primal_stone_name}</p>"
    else:
        return f"<p>{first_paragraph}</p>"

def convert_to_float(value):
    try:
        value = value.replace(',', '.')
        return float(value)
    except ValueError as e:
        # Il peut être utile d'ajouter un log ou d'lever une exception
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
    return write_description(product_info, first_paragraph)

def write_description(product_info, first_paragraph):
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
