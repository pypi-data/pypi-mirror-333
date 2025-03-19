# Drakkar Odoo Init

Outil d'initialisation de projets Odoo pour Drakkar.

## Installation

```bash
pip install drakkar-odoo-init
```

## Utilisation

Pour initialiser un nouveau projet Odoo :

```bash
drakkar-init
```

Pour initialiser dans un dossier spécifique :

```bash
drakkar-init --path /chemin/vers/projet
```

## Structure créée

L'outil crée la structure suivante :

```
.
├── config/
│   └── odoo.conf
├── drakkar-addons/
└── extra-addons/
```

## Configuration

Le fichier `odoo.conf` est configuré avec les paramètres par défaut pour un environnement de développement. 