# Récupération des package utilisés
pip3 freeze > requirements.txt

# Désactivation de l'environnement temporaire
deactivate

# Suppression du dossier de l'environnement temporaire
rm -r env_temp

# Suppression du dossier de copy data
rm -r data

#Suppression du dossier __pycache__
rm -r __pycache__