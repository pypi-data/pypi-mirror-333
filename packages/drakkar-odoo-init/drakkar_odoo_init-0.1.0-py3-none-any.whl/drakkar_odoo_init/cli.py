import argparse
from pathlib import Path
from .setup import OdooProjectSetup # type: ignore

def main():
    parser = argparse.ArgumentParser(
        description="Initialise un nouveau projet Odoo avec la configuration Drakkar"
    )
    parser.add_argument(
        "-p", 
        "--path", 
        default=".",
        help="Chemin où créer le projet (par défaut: dossier courant)"
    )
    
    args = parser.parse_args()
    setup = OdooProjectSetup(args.path)
    setup.setup() 