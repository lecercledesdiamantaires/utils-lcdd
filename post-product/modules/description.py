import logging

logging.basicConfig(filename='post-product/logs/post.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def check_first_paragraph(first_paragraph, product_type, primal_stone_name):
    """
    Vérifie et génère le premier paragraphe de la description du produit.
    """
    try:
        if not product_type:
            raise ValueError("Le type de produit est obligatoire")
            
        if product_type in ["Baguecatalogue", "Colliercatalogue", "Braceletcatalogue", "Boucledoreillescatalogue"]:
            primal_stone_name = "la pierre principale de votre choix, sertie sur une monture en Or de la couleur de votre choix. Si les options proposées ne vous conviennent pas, remplissez le formulaire de personnalisation pour découvrir des possibilités infinies."

        readable_type = product_type
        if product_type == 'Baguecatalogue':
            readable_type = "bague"
        elif product_type == 'Colliercatalogue':
            readable_type = "collier"
        elif product_type == 'Braceletcatalogue':
            readable_type = "bracelet"
        elif product_type == 'Boucledoreillescatalogue':
            readable_type = "boucle d'oreille"
        
        if not first_paragraph:
            if not primal_stone_name:
                logging.warning(f"Pierre principale manquante pour le produit de type {product_type}")
                primal_stone_name = "pierres précieuses"
            return f"<p>Découvrez notre {readable_type} en Or avec {primal_stone_name}</p>"
        else:
            return f"<p>{first_paragraph}</p>"
    except Exception as e:
        logging.error(f"Erreur lors de la génération du premier paragraphe: {str(e)}")
        raise ValueError(f"Erreur lors de la génération du premier paragraphe: {str(e)}")


def convert_to_float(value):
    """
    Convertit une valeur en nombre flottant avec gestion d'erreur améliorée.
    """
    if value is None:
        logging.warning("Valeur nulle détectée, utilisation de 0.0 par défaut")
        return 0.0
        
    if isinstance(value, (int, float)):
        logging.debug(f"Valeur {value} déjà convertie en nombre")
        return float(value)
        
    try:
        # Nettoyage de la valeur
        if isinstance(value, str):
            value = value.strip()
            if not value:
                logging.warning("Chaîne vide détectée, utilisation de 0.0 par défaut")
                return 0.0
                
            value = value.replace(',', '.')
            value = value.replace(' ', '')
            return float(value)
        else:
            raise TypeError(f"Type non supporté: {type(value)}")
    except (ValueError, TypeError) as e:
        error_msg = f"Impossible de convertir '{value}' en nombre: {str(e)}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def check_secondary_stones(secondary_stone_name, secondary_stone_carat):
    """
    Vérifie et formate les informations sur les pierres secondaires.
    """
    stones = []
    
    if not secondary_stone_name or not secondary_stone_carat:
        logging.debug("Pas de pierres secondaires ou informations incomplètes")
        return stones
        
    try:
        if ", " in secondary_stone_name:
            names = secondary_stone_name.split(", ")
            carats = secondary_stone_carat.split("-")
            
            if len(names) != len(carats):
                logging.warning(f"Nombre incohérent de noms ({len(names)}) et de carats ({len(carats)}) pour les pierres secondaires")
                
            # Utiliser le minimum des deux longueurs
            for i in range(min(len(names), len(carats))):
                try:
                    carat = convert_to_float(carats[i])
                    if names[i].strip():  # Vérifier que le nom n'est pas vide
                        stones.append({"name": names[i].strip(), "carat": carat})
                except ValueError as e:
                    logging.error(f"Erreur lors du traitement de la pierre secondaire {names[i]}: {str(e)}")
        else:
            try:
                carat = convert_to_float(secondary_stone_carat)
                if secondary_stone_name.strip():  # Vérifier que le nom n'est pas vide
                    stones.append({
                        "name": secondary_stone_name.strip(),
                        "carat": carat
                    })
            except ValueError as e:
                logging.error(f"Erreur lors du traitement de la pierre secondaire {secondary_stone_name}: {str(e)}")
                
        return stones
    except Exception as e:
        logging.error(f"Erreur inattendue lors du traitement des pierres secondaires: {str(e)}")
        return stones  # Retourner une liste vide en cas d'erreur pour éviter de bloquer le processus


def write_secondary_stones(secondary_stones):
    """
    Génère le HTML pour les pierres secondaires.
    """
    if not secondary_stones:
        return ""
    
    try:
        def format_stone(stone):
            carat_unit = "carat" if stone['carat'] < 2 else "carats"
            return f"{stone['name']} ({stone['carat']} {carat_unit})"

        title = "<strong>Pierres secondaires</strong>" if len(secondary_stones) > 1 else "<strong>Pierre secondaire</strong>"
        formatted_stones = ", ".join(format_stone(stone) for stone in secondary_stones)

        return f"<li>{title} : {formatted_stones}</li>"
    except Exception as e:
        logging.error(f"Erreur lors de la génération du HTML pour les pierres secondaires: {str(e)}")
        return ""  # Retourner une chaîne vide en cas d'erreur pour éviter de bloquer le processus


def generate_product_info(weight, primal_stone_name, carat_primal_stone, secondary_stone_name, 
                          carat_secondary_stone, stone_number, stone_shape, product_type, 
                          main_color, secondary_color, first_paragraph=None):
    """
    Génère la description complète du produit avec validation améliorée.
    """
    try:
        # Vérification des champs obligatoires
        if not product_type:
            raise ValueError("Le type de produit est obligatoire")
            
        if not primal_stone_name and product_type not in ["Baguecatalogue", "Colliercatalogue", "Braceletcatalogue", "Boucledoreillescatalogue"]:
            raise ValueError("La pierre principale est obligatoire pour ce type de produit")
        
        # Conversion des valeurs numériques
        try:
            weight = convert_to_float(weight) if weight else 0.0
        except ValueError as e:
            logging.error(f"Erreur de conversion du poids: {str(e)}")
            weight = 0.0
            
        try:
            carat_primal_stone = convert_to_float(carat_primal_stone) if carat_primal_stone else 0.0
        except ValueError as e:
            logging.error(f"Erreur de conversion du caratage de la pierre principale: {str(e)}")
            carat_primal_stone = 0.0
        
        # Génération du premier paragraphe
        first_paragraph = check_first_paragraph(first_paragraph, product_type, primal_stone_name)
        
        # Traitement des pierres secondaires
        secondary_stones = check_secondary_stones(secondary_stone_name, carat_secondary_stone)
        
        # Structuration des informations du produit
        product_info = {
            "weight": weight,
            "primal_stone": {
                "name": primal_stone_name or "Non spécifié", 
                "carat": carat_primal_stone,
                "color": main_color or "Non spécifié"
            },
            "secondary_stones": secondary_stones,
            "stone_number": stone_number,
            "stone_shape": stone_shape,
            "main_color": main_color or "Non spécifié",
            "secondary_color": secondary_color
        }
        
        # Génération de la description
        return write_description(product_info, first_paragraph, product_type)
    except Exception as e:
        error_msg = f"Erreur lors de la génération de la description du produit: {str(e)}"
        logging.error(error_msg)
        raise ValueError(error_msg)


def write_description(product_info, first_paragraph, product_type):
    """
    Génère le HTML de la description du produit.
    """
    try:
        if not product_type:
            raise ValueError("Le type de produit est obligatoire pour générer la description")
            
        if product_type in ["Baguecatalogue", "Colliercatalogue", "Braceletcatalogue", "Bouclesdoreillescatalogue"]:
            description = f"""
            {first_paragraph}
            <div class="infos-product">
                <h4>Caractéristiques du produit</h4>
                <ul>
                    <li><strong>Poids</strong> : Le poids dépend des options que vous choisirez. </li>
                    <li><strong>Matériau</strong> : Or de votre choix</li>
                    <li><strong>Pierre principale</strong> : Pierre principale au choix ({product_info['primal_stone']['carat']} {"carat" if product_info['primal_stone']['carat'] < 2 else "carats"})</li>
                    <li><strong>Couleur principale</strong>: Au choix</li>
                    {write_secondary_stones(product_info['secondary_stones'])}
                    {f"<li><strong>Nombre de pierres</strong> : {product_info['stone_number']}</li>" if product_info.get('stone_number') else ""}
                    {f"<li><strong>Couleur secondaire</strong> : {product_info['secondary_color']}</li>" if product_info.get('secondary_color') else ""}
                    {f"<li><strong>Forme de la pierre</strong> : {product_info['stone_shape']}</li>" if product_info.get('stone_shape') else ""}
                </ul>
            </div>
            <br>
            <p>Photos retouchées</p>
            """
        else:
            description = f"""
            {first_paragraph}
            <div class="infos-product">
                <h4>Caractéristiques du produit</h4>
                <ul>
                    <li><strong>Poids</strong> : {product_info['weight']} {"gramme" if product_info['weight'] < 2 else "grammes"}</li>
                    <li><strong>Matériau</strong> : Or</li>
                    <li><strong>Pierre principale</strong> : {product_info['primal_stone']['name']} ({product_info['primal_stone']['carat']} {"carat" if product_info['primal_stone']['carat'] < 2 else "carats"})</li>
                    <li><strong>Couleur principale</strong> : {product_info['main_color']}</li>
                    {write_secondary_stones(product_info['secondary_stones'])}
                    {f"<li><strong>Nombre de pierres</strong> : {product_info['stone_number']}</li>" if product_info.get('stone_number') else ""}
                    {f"<li><strong>Couleur secondaire</strong> : {product_info['secondary_color']}</li>" if product_info.get('secondary_color') else ""}
                    {f"<li><strong>Forme de la pierre</strong> : {product_info['stone_shape']}</li>" if product_info.get('stone_shape') else ""}
                </ul>
            </div>
            <br>
            <p>Photos retouchées</p>
            """
        return description
    except Exception as e:
        error_msg = f"Erreur lors de la génération du HTML de la description: {str(e)}"
        logging.error(error_msg)
        raise ValueError(error_msg)