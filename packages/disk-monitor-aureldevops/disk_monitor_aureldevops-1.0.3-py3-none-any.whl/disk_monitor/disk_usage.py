import shutil

def check_disk_usage(path="/"):
    """
    Vérifie l'espace disque disponible sur un chemin spécifié

    Args:
        path (str): Le chemin du répertoire ou disque à vérifier. Par défaut, il s'agit de la racine ("/"),
                    qui correspond au disque principal du système.

    Returns:
        tuple: Un tuple contenant trois valeurs en octets:
            - total (int) : l'espace disque total du chemin spécifié,
            - used (int) : l'espace disque déjà utilisé,
            - free (int) : l'espace disque encore disponible.
            
    Exemple:
        >>> total, used, free = check_disk_usage("/")
        >>> print(f"Total: {total} octets, Utilisé: {used} octets, Libre: {free} octets")
    """
    total, used, free = shutil.disk_usage(path)
    return total, used, free