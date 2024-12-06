def tags(product_type, primal_stone_name, secondary_stone_name):
    if "-" in secondary_stone_name:
        secondary_stone_name = ", ".join([s.capitalize() for s in secondary_stone_name.split("-")])
    else:
        secondary_stone_name = secondary_stone_name.capitalize()

    tags = f"{product_type.capitalize()}, {primal_stone_name.capitalize()}, {secondary_stone_name}, Or blanc, Or jaune, Or rose."
    
    return tags
