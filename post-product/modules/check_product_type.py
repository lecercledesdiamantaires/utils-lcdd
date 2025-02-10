AVAILABLE_RODUCT_TYPES = [
    'Bague', 'Collier', 'Bracelet', 'Broche', 'Puce', 'Pendantes', 'Diamant', 'Alliance'
]

def check_product_type(product_id, product_type):
    """
    Fonction pour vérifier si le type de produit est valide.
    
    Arguments:
    product_id -- l'identifiant du produit
    product_type -- le type de produit à vérifier
    
    Lève une exception ValueError si le type de produit est invalide.
    """
    formatted_type = product_type.strip().capitalize() 
    
    if formatted_type not in AVAILABLE_RODUCT_TYPES:
        raise ValueError(f"Le type de produit '{formatted_type}' n'est pas valide. ID du produit : {product_id}.")