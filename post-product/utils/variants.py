from options import create_options


def select_price(price, product_option) : 
    if product_option == '14':
        price = int(price) * 0.85
    return str(price)


def create_variants(price, type):
    options = create_options(type)
    variants = []
    for option1 in options[0]['values']:
        for option2 in options[1]['values']:
            if len(options) >= 3:
                for option3 in options[2]['values']:
                    variant = {
                        "option1": option1,
                        "option2": option2,
                        "option3": option3,
                        "price" : select_price(price, option3)
                    }
                    variants.append(variant)
            else: 
                variant = {
                    "option1": option1,
                    "option2": option2,
                    "price" : select_price(price, option2)
                }
                variants.append(variant)
    print(variants)
    print(len(variants))
        
        
create_variants('1000')