from options import create_options


def select_price(price, product_option) : 
    if product_option == '14':
        price = int(price) * 0.85
    return str(price)


def create_variants(price, prodct_type, weight):
    options = create_options(prodct_type)
    variants = []
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
                        "inventory_quantity": 999,
                        "old_inventory_quantity": 999,
                    }
                    variants.append(variant)
            else: 
                variant = {
                    "option1": option1,
                    "option2": option2,
                    "price" : select_price(price, option2),
                    "weight": weight,
                    "inventory_quantity": 999,
                    "old_inventory_quantity": 999,
                }
                variants.append(variant)
    return variants
    # print(variants)
    # print(len(variants))
        
        
