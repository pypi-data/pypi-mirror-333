from pathlib import Path
import shutil
import sys

class OdooProjectSetup:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.folders = ["config", "drakkar-addons", "extra-addons"]
        
    def create_directory_structure(self):
        """Crée la structure de base des dossiers"""
        print("🚀 Création de la structure des dossiers...")
        
        for folder in self.folders:
            folder_path = self.base_path / folder
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Dossier créé : {folder}")
            except Exception as e:
                print(f"❌ Erreur lors de la création du dossier {folder}: {e}")
                sys.exit(1)
            
    def create_odoo_config(self):
        """Crée le fichier de configuration Odoo par défaut"""
        print("\n📝 Création du fichier odoo.conf...")
        
        config_content = """[options]
addons_path = /mnt/extra-addons,/mnt/drakkar-addons
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
"""
        
        config_path = self.base_path / "config" / "odoo.conf"
        try:
            with open(config_path, "w") as f:
                f.write(config_content)
            print("✅ Fichier odoo.conf créé")
        except Exception as e:
            print(f"❌ Erreur lors de la création du fichier odoo.conf: {e}")
            sys.exit(1)

    def setup(self):
        """Exécute toute la configuration"""
        print("🎉 Démarrage de la configuration du projet Odoo...")
        self.create_directory_structure()
        self.create_odoo_config()
        print("\n✨ Configuration terminée avec succès!") 