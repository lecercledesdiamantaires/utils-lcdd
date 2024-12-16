def check_first_p(first_p, product_type, primal_stone_name) :
    if not first_p  :
        return f"<p>Découvrez notre {product_type} en Or avec {primal_stone_name}</p>"
    else :
        return f"<p>{first_p}</p>"

def convert_to_float(value):
    try:
        # Remplacer les virgules par des points
        value = value.replace(',', '.')
        # Convertir la chaîne en float
        return float(value)
    except ValueError as e:
        print(f"Erreur de conversion : {e}")
        return None

def check_secondary_stone(secondary_stone_name, secondary_stone_carat) :
    secondary_stone = []
    if "-" in secondary_stone_name :
        names = secondary_stone_name.split(", ")
        carats = secondary_stone_carat.split(", ")
        for name, carat in zip(names, carats) :
            secondary_stone.append({
                "name": name,
                "carat": carat
            })
    else :
        secondary_stone.append({
            "name": secondary_stone_name,
            "carat": secondary_stone_carat
        })
    return secondary_stone


def write_secondary_stone(secondary_stones):
    def format_stone(stone):
        carat_unit = "carat" if stone['carat'] < 2 else "carats"
        print(stone['carat'])
        return f"{stone['name']} ({stone['carat']} {carat_unit})"

    if not secondary_stones:
        return ""
    
    title = "<strong>Pierres secondaires</strong>" if len(secondary_stones) > 1 else "<strong>Pierre secondaire</strong>"


    formatted_stones = ", ".join(format_stone(stone) for stone in secondary_stones)

    return f"""
    <li>{title} : {formatted_stones}</li>
    """
        
def write_description(product_info, first_p) :
    description = f"""
    {first_p}
    <div class="infos-product">
        <h4>Caractéristiques du produit</h4>
        <!--short-description-->
        <ul>
            <li><strong>Poids </strong>: {product_info['weight']} {"gramme" if float(product_info['weight']) < 2 else "grammes"}</li>
            <li><strong>Matériau </strong>: Or</li>
            <li><strong>Pierre principale </strong>: {product_info['primal_stone']['name']} ({product_info['primal_stone']['carat']} {"carat" if float(product_info['primal_stone']['carat']) < 2 else "carats"})</li>
            {write_secondary_stone(product_info['secondary_stone'])}
            <li><strong>Nombre de pierres </strong>: {product_info['stone_number']}</li>
            <li><strong>Couleur principale </strong>: {product_info['main_color']}</li>
            <li><strong>Couleur secondaire </strong>: {product_info['secondary_color']}</li>
            <li><strong>Forme de la pierre </strong>: {product_info['stone_shape']}</li>
        </ul>
        <!--end-short-description-->
    </div>
    <br>
    <p>Photos retouchées</p>
    """
    return description

def main(
    weight, 
    primal_stone_name, 
    carat_primal_stone, 
    secondary_stone_name, 
    carat_secondary_stone, 
    stone_number, 
    stone_shape, 
    product_type,
    main_color,
    secondary_color,
    first_p=None) :

    weight = convert_to_float(weight)
    carat_primal_stone = convert_to_float(carat_primal_stone)
    carat_secondary_stone = convert_to_float(carat_secondary_stone)
    first_p = check_first_p(first_p, product_type, primal_stone_name)
    secondary_stone = check_secondary_stone(secondary_stone_name, carat_secondary_stone)
  
    product_info = {
        "weight": weight,
        "primal_stone": 
            {
                "name" : primal_stone_name,
                "carat" : carat_primal_stone
            },
        "secondary_stone": secondary_stone,
        "stone_number": stone_number,
        "stone_shape": stone_shape,
        "main_color": main_color,
        "secondary_color": secondary_color
    }
    return write_description(product_info, first_p)
