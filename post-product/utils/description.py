def check_first_p(first_p, product_type, primal_stone_name) :
    if not first_p  :
        return f"<p>Découvrez notre {product_type} en Or avec {primal_stone_name}</p>"
    else :
        return f"<p>{first_p}</p>"

def check_secondary_stone(secondary_stone_name, secondary_stone_carat) :
    secondary_stone = []
    if "-" in secondary_stone_name :
        names = secondary_stone_name.split("-")
        carats = secondary_stone_carat.split("-")
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
        carat_unit = "carat" if float(stone['carat']) < 1 else "carats"
        return f"{stone['name']} ({stone['carat']} {carat_unit})"

    if not secondary_stones:
        return ""
    
    title = "Pierres secondaires" if len(secondary_stones) > 1 else "Pierre secondaire"


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
            <li><strong>Poids </strong>: {product_info['weight']} {"gramme" if product_info['weight'] <1 else "grammes"}</li>
            <li><strong>Matériau </strong>: {product_info['material']}</li>
            <li><strong>Pierre principale </strong>: {product_info['primal_stone']['name']} {product_info['primal_stone']['color']}({product_info['primal_stone']['carat']} {"carat" if product_info['primal_stone']['carat'] < 1 else "carats"})</li>
            {write_secondary_stone(product_info['secondary_stone'])}
            <li><strong>Nombre de pierres </strong>: {product_info['stone_number']}</li>
            <li><strong>Forme de la pierre </strong>: {product_info['stone_shape']}</li>
            <li><strong>Type de serti </strong>: {product_info['serti_type']}</li>
        </ul>
        <!--end-short-description-->
    </div>
    <br>
    <p>Photos retouchées</p>
    """
    return description

def main(
    weight, 
    material, 
    primal_stone_name, 
    carat_primal_stone, 
    secondary_stone_name, 
    carat_secondary_stone, 
    stone_number, 
    stone_shape, 
    serti_type,
    product_type,
    main_stone_color,
    first_p=None) :

    first_p = check_first_p(first_p, product_type, primal_stone_name)
    secondary_stone = check_secondary_stone(secondary_stone_name, carat_secondary_stone)
    product_info = {
        "weight": weight,
        "material": material,
        "primal_stone": 
            {
                "name" : primal_stone_name,
                "carat" : carat_primal_stone,
                "color" : main_stone_color
            },
        "secondary_stone": secondary_stone,
        "stone_number": stone_number,
        "stone_shape": stone_shape,
        "serti_type": serti_type
    }
    return write_description(product_info, first_p)

# print(main(
#     2.5,
#     "Or jaune",
#     "Diamant",
#     0.5,
#     "Saphir-Rubis",
#     "0.3-0.4",
#     3,
#     "Rond",
#     "Pavé",
#     "Bague",
#     "OUi oui oui"
# ))