from options import create_options


def create_variants():
    options = create_options()
    variants = []
    for option1 in options[0]['values']:
        for option2 in options[1]['values']:
            if len(options) >= 3:
                for option3 in options[2]['values']:
                    variant = {
                        "option1": option1,
                        "option2": option2,
                        "option3": option3
                    }
                    variants.append(variant)
            else: 
                variant = {
                    "option1": option1,
                    "option2": option2
                }
                variants.append(variant)
    print(variants)
    print(len(variants))
        
        
create_variants()