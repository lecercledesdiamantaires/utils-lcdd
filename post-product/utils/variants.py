from options import create_options


def select_price(price, product_option) : 
    if product_option == '14':
        price = int(price) * 0.85
    return str(price)

def convert_to_float(value):
    try:
        # Remplacer les virgules par des points
        value = value.replace(',', '.')
        # Convertir la chaîne en float
        return float(value)
    except ValueError as e:
        print(f"Erreur de conversion : {e}")
        return None


def create_variants(price, prodct_type, weight):
    options = create_options(prodct_type)
    variants = []
    weight = convert_to_float(weight)
    for option1 in options[0]['values']:
        for option2 in options[1]['values']:
            if len(options) >= 3:
                for option3 in options[2]['values']:
                    variant = {
                        "option1": option1,
                        "option2": option2,
                        "option3": option3,
                        "inventory_policy": "continue",
                        "barcode": "", 
                        "inventory_management": "shopify",
                        "price" : select_price(price, option3),
                        "weight": weight,
                        "weight_unit": "g",
                        "inventory_quantity": 999,
                        "old_inventory_quantity": 999,
                    }
                    variants.append(variant)
            else: 
                variant = {
                    "option1": option1,
                    "option2": option2,
                    "option3": "null",
                    "inventory_policy": "continue",
                    "barcode": "", 
                    "inventory_management": "shopify",
                    "price" : select_price(price, option2),
                    "weight": weight,
                    "weight_unit": "g",
                    "inventory_quantity": 999,
                    "old_inventory_quantity": 999,
                }
                variants.append(variant)
    return variants
    # print(variants)
    # print(len(variants))
        
        
