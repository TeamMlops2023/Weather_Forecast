# Copy du fichier data dans le fichier src (à supprimer une fois le code corrigé)
cp -r ../../data .

# Création de l'environnement temporaire
python3 -m venv env_temp

# Activation de l'environnement temporaire
source env_temp/bin/activate

# Importation des packages nécessaire via requirements.txt
pip install --no-cache-dir -r requirements.txt

# Suppression du fichier modele_logs.log de la session précédente
rm modele_logs.log

# Exécution du code fastapi
uvicorn app:app --reload
