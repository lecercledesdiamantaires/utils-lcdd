from get_infos import get_infos

infos=[]

def get_price(infos):
    infos = get_infos()
    for info in infos:
        forteen_carats = int(info['price']) * 0.85
    return str(forteen_carats)

get_price(infos)