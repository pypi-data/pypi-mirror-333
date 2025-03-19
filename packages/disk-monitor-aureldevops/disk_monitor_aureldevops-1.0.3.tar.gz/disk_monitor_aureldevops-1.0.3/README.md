# Démo : Créer et publier un module Python multi-fichiers

## Contexte

Nous allons structurer un module de surveillance disque avancé, appelé `disk_monitor`. Il sera composé de plusieurs fichiers pour une meilleure organisation et contiendra des métadonnées comme la version et l'auteur. Ensuite, nous verrons comment l'utiliser dans un script, puis comment le publier sur PyPI.

## Structure du projet

Organisons le projet comme suit :

```tree
disk_monitor_project/
├── disk_monitor/
│   ├── __init__.py
│   ├── __version__.py
│   ├── alert.py
│   └── disk_usage.py
├── monitor_script.py
└── setup.py
```

- **disk_monitor/** : dossier principal contenant les fichiers du module.
- **monitor_script.py** : script qui va utiliser le module `disk_monitor`.
- **setup.py** : fichier de configuration pour publier le module sur PyPI.
- `__init__.py` : initialise notre contenu comme un module (possibilité d'importer)
- `__version__.py` : fichier contenant des metadonnées
- `alert.py` : script affichant des messages à l'utilisateur
- `disk_usage.py` : script contenant des fonctions de vérification

---

# Todo

- [ ] créer les fichiers du module
- [ ] utiliser le module dans un script
- [ ] préparer un fichier de setup pour PyPi
- [ ] publier le module sur PyPi