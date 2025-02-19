import os
import requests
import random
from dotenv import load_dotenv
import streamlit as st

API_KEY = st.secrets["API_KEY"]
PASSWORD = st.secrets["PASSWORD"]
SHOP_NAME = st.secrets["SHOP_NAME"]
API_VERSION = st.secrets["API_VERSION"]
LIMIT = st.secrets["LIMIT"]
FALSE_URL = st.secrets["FALSE_URL"]
SHOPIFY_STORE = st.secrets["SHOP_URL"]

all_products = []

stone_metafields = [
    { "id": "\"gid://shopify/Metaobject/85147255119\"", "stone": "Chrysoprase" },
    { "id": "\"gid://shopify/Metaobject/85096694095\"", "stone": "Corail" },
    { "id": "\"gid://shopify/Metaobject/83813859663\"", "stone": "Agate" },
    { "id": "\"gid://shopify/Metaobject/83815203151\"", "stone": "Opaline" },
    { "id": "\"gid://shopify/Metaobject/83815170383\"", "stone": "Turquoise" },
    { "id": "\"gid://shopify/Metaobject/83815039311\"", "stone": "Spinelle" },
    { "id": "\"gid://shopify/Metaobject/83814941007\"", "stone": "Rubellite" },
    { "id": "\"gid://shopify/Metaobject/83814908239\"", "stone": "Rhodonite" },
    { "id": "\"gid://shopify/Metaobject/83814875471\"", "stone": "Pyrite" },
    { "id": "\"gid://shopify/Metaobject/83814842703\"", "stone": "Pierre de lune" },
    { "id": "\"gid://shopify/Metaobject/83814777167\"", "stone": "Péridot" },
    { "id": "\"gid://shopify/Metaobject/83814744399\"", "stone": "Opale" },
    { "id": "\"gid://shopify/Metaobject/83814711631\"", "stone": "Onyx" },
    { "id": "\"gid://shopify/Metaobject/83814678863\"", "stone": "Oeil de tigre"},
    { "id": "\"gid://shopify/Metaobject/83814646095\"", "stone": "Nacre" },
    { "id": "\"gid://shopify/Metaobject/83814580559\"", "stone": "Lapis Lazuli" },
    { "id": "\"gid://shopify/Metaobject/83814547791\"", "stone": "Labradorite" },
    { "id": "\"gid://shopify/Metaobject/83814515023\"", "stone": "Kyanite" },
    { "id": "\"gid://shopify/Metaobject/83814449487\"", "stone": "Jade" },
    { "id": "\"gid://shopify/Metaobject/83814383951\"", "stone": "Iolite" },
    { "id": "\"gid://shopify/Metaobject/83814318415\"", "stone": "Grenat" },
    { "id": "\"gid://shopify/Metaobject/83814285647\"", "stone": "Cornaline" },
    { "id": "\"gid://shopify/Metaobject/83814220111\"", "stone": "Calcédoine" },
    { "id": "\"gid://shopify/Metaobject/83814154575\"", "stone": "Aventurine" },
    { "id": "\"gid://shopify/Metaobject/83813990735\"", "stone": "Ambre" },
    { "id": "\"gid://shopify/Metaobject/83813957967\"", "stone": "Amazonite" },
    { "id": "\"gid://shopify/Metaobject/83801538895\"", "stone": "Topaze" },
    { "id": "\"gid://shopify/Metaobject/83801440591\"", "stone": "Tanzanite" },
    { "id": "\"gid://shopify/Metaobject/83800850767\"", "stone": "Saphir" },
    { "id": "\"gid://shopify/Metaobject/83800555855\"", "stone": "Tourmaline" },
    { "id": "\"gid://shopify/Metaobject/83799474511\"", "stone": "Quartz" },
    { "id": "\"gid://shopify/Metaobject/83799441743\"", "stone": "Perle" },
    { "id": "\"gid://shopify/Metaobject/83797410127\"", "stone": "Émeraude" },
    { "id": "\"gid://shopify/Metaobject/83797279055\"", "stone": "Citrine" },
    { "id": "\"gid://shopify/Metaobject/83795935567\"", "stone": "Améthyste" },
    { "id": "\"gid://shopify/Metaobject/83795837263\"", "stone": "Diamant" },
    { "id": "\"gid://shopify/Metaobject/83795804495\"", "stone": "Aigue-Marine" },
    { "id": "\"gid://shopify/Metaobject/83795214671\"", "stone": "Morganite" },
    { "id": "\"gid://shopify/Metaobject/83532054863\"", "stone": "Rubis" },
    { "id": "\"gid://shopify/Metaobject/292354818383\"", "stone": "Spessarite"},
    { "id": "\"gid://shopify/Metaobject/292394041679\"", "stone": "Tsavorite"}
]

color_metafields = [
    { "id": "\"gid://shopify/Metaobject/85293171023\"", "color": "bleu" },
    { "id": "\"gid://shopify/Metaobject/85289992527\"", "color": "vert" },
    { "id": "\"gid://shopify/Metaobject/85161443663\"", "color": "violet" },
    { "id": "\"gid://shopify/Metaobject/83803111759\"", "color": "blanc" },
    { "id": "\"gid://shopify/Metaobject/85293695311\"", "color": "rouge" },
    { "id": "\"gid://shopify/Metaobject/84184858959\"", "color": "jaune" },
    { "id": "\"gid://shopify/Metaobject/83803308367\"", "color": "rose" },
    { "id": "\"gid://shopify/Metaobject/299818778959\"", "color": "noir" },
    { "id": "\"gid://shopify/Metaobject/85294874959\"", "color": "multicolore" },
    { "id": "\"gid://shopify/Metaobject/85298184527\"", "color": "orange" },
    { "id": "\"gid://shopify/Metaobject/301276856655\"", "color": "argent" }
]


def load_products():
    """
    Charge tous les produits de tous les types depuis Shopify une seule fois.
    Les produits sont stockés dans la variable globale `all_products`.
    """
    global all_products
    url = f"https://{API_KEY}:{PASSWORD}@{SHOPIFY_STORE}/admin/api/2024-01/products.json"
    page_info = None

    while True:
        paginated_url = url
        if page_info:
            paginated_url += f"?page_info={page_info}"

        response = requests.get(paginated_url)
        response.raise_for_status()
        data = response.json()

        all_products.extend(data.get("products", []))

        next_page_info = response.links.get("next", {}).get("url")
        if next_page_info:
            page_info = next_page_info.split("page_info=")[-1]
        else:
            break

def enlever_doublons(liste):
    # Utiliser un set pour supprimer les doublons et conserver l'ordre d'origine
    liste_sans_doublons = list(dict.fromkeys(liste))
    return liste_sans_doublons

def find_products_by_type(product_type):
    """
    Recherche dans les produits déjà chargés ceux correspondant à un type donné.
    """
    return [product for product in all_products if product.get("product_type") == product_type]


def select_two_random_ids(related_products):
    """
    Sélectionne deux IDs au hasard parmi les produits chargés dans `all_products`.
    """
    if len(related_products) < 2:
        raise ValueError("Pas assez de produits pour sélectionner deux éléments au hasard.")
    
    # Sélectionner deux IDs au hasard
    random_products = random.sample(related_products, 2)  
    return random_products[0]["id"], random_products[1]["id"]

def get_related_products(product_type):
    """
    Sélectionne deux produits de type 'product_type' et retourne leurs IDs.
    """
    related_products = find_products_by_type(product_type)
    id1, id2 = select_two_random_ids(related_products)

    return f"[\"gid://shopify/Product/{id1}\",\"gid://shopify/Product/{id2}\"]"


def get_gold_color():
    """
    Retourne l'ID de la couleur "Or" dans Shopify.
    """
    return "[\"gid://shopify/Metaobject/83803111759\",\"gid://shopify/Metaobject/84184858959\",\"gid://shopify/Metaobject/83803308367\"]"

def get_stone(primal_stone, secondary_stone):
    """
    Retourne les IDs des pierres principales et secondaires dans Shopify.
    Gestion de la casse pour éviter les problèmes avec majuscules/minuscules.
    """
    # Transformer la chaîne secondary_stone en liste avec séparation par tirets et tout en minuscule
    secondary_stone_list = [stone.lower() for stone in secondary_stone.split(', ')]

    # Liste pour stocker les IDs
    stone_ids = []

    for stone in stone_metafields:
        if stone["stone"].lower() == primal_stone.lower():
            stone_ids.append(stone["id"])
        for i in range (len(secondary_stone_list)):
            if stone["stone"].lower() in secondary_stone_list:
                secondary_stone_list.remove(stone["stone"].lower())
                stone_ids.append(stone["id"])

    return stone_ids
    
def get_color(primal_color, secondary_color):
    """
    Retourne les IDs des couleurs principales et secondaires dans Shopify.
    Gestion de la casse pour éviter les problèmes avec majuscules/minuscules.
    """
    # Transformer la chaîne secondary_color en liste avec séparation par tirets et tout en minuscule
    secondary_color_list = [color.lower() for color in secondary_color.split(', ')]
    
    # Liste pour stocker les IDs
    color_ids = []
    
    for color in color_metafields:
        if color["color"].lower() == primal_color.lower():
            color_ids.append(color["id"])
        for i in range(len(secondary_color_list)):
            if color["color"].lower() in secondary_color_list:
                secondary_color_list.remove(color["color"].lower())
                color_ids.append(color["id"])

    return color_ids

def formater_liste(liste):
    # Supprimer les guillemets internes et formater la liste
    resultat = [element.strip('"') for element in liste]
    return "[" + ",".join(f'"{elem}"' for elem in resultat) + "]"

def get_metafield(product_type, primal_stone, secondary_stone, color, secondary_color):
    """
    Retourne les IDs des metafields pour les pierres et les couleurs.
    """
    load_products()

    stone_ids = enlever_doublons(get_stone(primal_stone, secondary_stone))
    color_ids = enlever_doublons(get_color(color, secondary_color))
    gold_color = get_gold_color()
    related_products = get_related_products(product_type)

    return [
            {
                "namespace": "custom",
                "key": "pierre_pr_cieuse",
                "value": formater_liste(stone_ids),
                "type": "list.metaobject_reference",
            },
            {
                "namespace": "custom",
                "key": "couleur_de_la_pierre",
                "value": formater_liste(color_ids),
                "type": "list.metaobject_reference",
            },
            {
                "namespace": "custom",
                "key": "couleur_de_l_or",
                "value": gold_color,
                "type": "list.metaobject_reference",
            },
            {
                "namespace": "related_products",
                "key": "product_list",
                "value": related_products,
                "value_type": "list.product_reference",
            }
        ]
    