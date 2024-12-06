available_product_types = ['Bague', 'Collier', 'Bracelet', 'Broche', 'Puce', 'Pendantes', 'Diamant', 'Alliance']   

def check_product_type(id, product_type):
    product_type = product_type.capitalize()
    if product_type not in available_product_types:
        raise ValueError(f"Le type de produit {product_type} n'est pas valide id : {id}.")

