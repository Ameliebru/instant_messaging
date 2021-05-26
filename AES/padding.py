
""" 
PKCS7 : Standard de syntaxe de message cryptographique pour notre fonction padding 
"""
# Fonction de padding 

def padding (text, size):
    # On verifie que la taille du texte est un multiple de size
    if len(text) % size != 0:
        # On cacule le nombre d'element qu'il faut ajouter 
        add = size - len(text) % size
        # On ajoute add éléments pour le padding
        for _ in range(add):
            text = text + chr(add)
    else:
        add = size
        for _ in range(add):
            text = text + chr(add)
    
    return text 

#Fonction pour enlever le padding 

def unpadding(text):
    # On prend le dernier caractère
    d = text[len(text) - 1]
    # Si d est un caractère de padding
    if d < 17:
    # Initialisation du nombre d'occurrence
        occ = 1
        # Pour tout élément du block
        for i in range(len(text) - 2, len(text) - 18, -1):
            # Si l'élément est le même que le dernier
            if text[i] == d:
                # Si il y en a plus que le chiffre de padding ce dernier est faux sinon on incrémente
                if occ > d:
                    return text
                else:
                    occ += 1
            else:
                if occ < d:
                    return text
                else: #On supprime le padding 
                    return text[:-occ]
    return text 
