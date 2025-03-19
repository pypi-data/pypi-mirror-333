from .disk_usage import check_disk_usage

def is_disk_full(path="/", threshold=10):
    """
    Vérifie si l'espace disque restant est en dessous d'un certain seuil.

    Args:
        path (str): Le chemin du disque ou répertoire à vérifier (par défaut, "/").
        threshold (int): Le seuil en pourcentage en dessous duquel on considère le disque comme plein.

    Returns:
        bool: `True` si l'espace libre est en dessous du seuil, sinon `False`.
    
    Exemple:
        >>> is_disk_full("/", 10)
        False  # si le disque a plus de 10% d'espace libre
    """
    # Utilise check_disk_usage pour obtenir l'espace total, utilisé et libre
    total, used, free = check_disk_usage(path)

    # Calcul du pourcentage d'espace libre
    free_percent = (free / total) * 100

    # Retourne True si le pourcentage d'espace libre est en dessous du seuil
    return free_percent < threshold

def alert_if_disk_full(path="/", threshold=10):
    """
    Affiche un message d'alerte si l'espace disque est insuffisant.

    Args:
        path (str): Le chemin du disque ou répertoire à vérifier (par défaut, "/").
        threshold (int): Le seuil en pourcentage pour l'alerte d'espace disque.

    Exemple:
        >>> alert_if_disk_full("/", 10)
        Attention : L'espace disque sur / est inférieur à 10% !
    """
    if is_disk_full(path, threshold):
        # Message d'alerte si l'espace libre est inférieur au seuil
        print(f"Attention : L'espace disque sur {path} est inférieur à {threshold}% !")
    else:
        # Message indiquant que l'espace disque est suffisant
        print(f"Espace disque suffisant sur {path}.")