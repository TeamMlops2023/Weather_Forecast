import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime


# Paramètres de réessai de connexion
max_attempts = 5
attempt_count = 0

def connection_base_sql(host: str = "database-service", 
                        user : str = "root", 
                        password : str = "mysecretpassword", 
                        database : str = "mlops_weather", 
                        max_attempts : int = 5, 
                        attempt_count : int = 0):
  """
    Établit une connexion à la base de données MySQL avec des tentatives répétées en cas d'échec.

    Parameters:
    - host (str): Adresse IP ou nom d'hôte du serveur de base de données.
    - user (str): Nom d'utilisateur pour la connexion à la base de données.
    - password (str): Mot de passe pour la connexion à la base de données.
    - database (str): Nom de la base de données à laquelle se connecter.
    - max_attempts (int): Nombre maximal de tentatives de connexion.
    - attempt_count (int): Compteur de tentatives actuel.

    Raises:
    - ExitException: Si la connexion échoue après plusieurs tentatives.

    Returns:
    - db (mysql.connector.connection.MySQLConnection): Objet de connexion à la base de données.
    - cursor (mysql.connector.cursor.MySQLCursor): Objet curseur pour exécuter des requêtes SQL.
    """
                          
  while attempt_count < max_attempts:
    try:
      # Connexion à la base de données
      db = mysql.connector.connect(host=host, user=user, password=password, database=database)
      print(f"Connecté à MySQL{database}")
      cursor = db.cursor()
      break
    except Error as e:
      print(f"Erreur lors de la connexion à MySQL {database}: {e}")
      attempt_count += 1
      time.sleep(5)  # Attendre 5 secondes avant de réessayer

  if attempt_count == max_attempts:
    print("Échec de la connexion à MySQL après plusieurs tentatives")
    exit(1)
    
  return db, cursor


def lecture_table_sql(db, date_du_jour):
    # Création d'une requête SQL pour sélectionner toutes les colonnes de la table spécifiée pour la date du jour
    query = f"SELECT * FROM weather_scraped WHERE day = '{current_date}'"

    try:
        # Lecture des données depuis la base de données dans un DataFrame
        df = pd.read_sql(query, db)
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture de la table weather_scraped : {e}")
        return None

    return df


def insertion_sql(data, db, cursor):

  """
    Insert les predictions dans une table MySQL.

    Parameters:
    - data: Probabilitees des predictions du modele.
    - db: Objet de connexion à la base de données.
    - cursor: Objet curseur pour exécuter des requêtes SQL.

  """
  
  for i in range(len(data)):
    date = data.iloc[i]['date']
    ville = data.iloc[i]['ville']
    proba = max(data.iloc[i][2:].values)
    # prediction = data_propre.iloc[0][2:].idxmax()   => Ne marche plus ?
    for i, val in enumerate(data.iloc[i][2:].values):
        if val == proba:
            prediction = data.iloc[0][2:].index[i]
            break
    
    insert_query = "INSERT INTO weather_predictions (date, ville, prediction, proba) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (date, ville, prediction, proba))

  db.commit()


def fermeture_sql(db, cursor):

  """
    Ferme une base sql avec le curseur.

    Parameters:
    - db: Objet de connexion à la base de données.
    - cursor: Objet curseur pour exécuter des requêtes SQL.
    
  """
  
  cursor.close()
  db.close()

  return print("Base SQL et curseur fermés")

def preparation_donne(df):

  """
    Prépare les données pour un modèle de prédiction de pluie.

  Parameters:
  - df: DataFrame contenant les données météorologiques.

  Actions:
  - Tri du DataFrame par 'ville' et 'day'.
  - Réinitialisation des indices.
  - Conversion des valeurs de 'rain' en 0 ou 1
  - Itération sur chaque ville pour traiter les valeurs de 'rain'.
  - Suppression des colonnes 'evap', 'sun', 'wind_dir', '9am_wind_dir', '3pm_wind_dir' pour simplifier le modèle
  - Séparation des variables cibles des features.

  Returns:
  - X: DataFrame des features.
  - y: Série des variables cibles 'rain_tomorrow'.
  """

  # Tri du DataFrame par 'ville' et 'day'
  df = df.sort_values(by=['ville', 'day'])

  # Réinitialisation des indices
  df = df.reset_index(drop=True)

  # Conversion des valeurs de 'rain' en 0 ou 1
  df['rain'] = df['rain'].apply(lambda x: 0 if x == '0' else 1)

  # Suppression de certaines colonnes pour simplifier le modèle dans le cadre du projet
  # 'evap', 'sun' sont souvent vides et 'wind_dir', '9am_wind_dir', '3pm_wind_dir' nécessitent un encodage particulier qu'on évite ici pour simplifier
  df = df.drop(['wind_dir', '9am_wind_dir', '3pm_wind_dir', 'evap', 'sun'], axis=1)

  # Séparation des variables ville et day
  df_prepro = df.drop(['ville', 'day'], axis=1)
  df_predi = df['ville', 'day']

  return df_prepro, df_predi


def load_model():

  """
    Charge le modèle le plus récent à partir des fichiers dans le dossier 'data'.

    Returns:
        object: L'objet du modèle chargé.
  """
  
  # Lecture des dates des différents modeles
  fichiers_model = [f for f in os.listdir('data') if f.startswith('model_')]

  # Recuperation du nom du modele le plus récent
  fichier_plus_recent = max(fichiers_model, key=lambda f: f.split('_v')[1].split('.csv')[0])
  chemin_dernier_model = os.path.join(dossier_data, fichier_plus_recent)

  # Récupération du modèle
  loaded_model = joblib.load(chemin_dernier_model)

  return loaded_model
  
################################################################################################################################################################################################################
################################################################################################################################################################################################################

# Connection à la base sql
db, cursor = connection_base_sql()

# Obtenez la date actuelle au format 'YYYYMMDD'
date_format = "%Y%m%d"
current_date = datetime.now().strftime(date_format)

# Construire le nom du fichier en ajoutant la date au modèle
# new_data_filename = 'data_scrapees_2.csv'

# Chemin vers le fichier de données
# chemin_fichier_donnees = os.path.join('data', new_data_filename)

# Charger les données à partir de la table sql des données scrapées
# df = pd.read_csv(chemin_fichier_donnees)
df = lecture_table_sql(db, current_date)

# Préparation des données
df_prepro, df_predi = preparation_donne(df)

# Chargement du dernier modele
loaded_model = load_model()

# Prédiction du modèle
proba_pluie = pd.DataFrame(loaded_model.predict_proba(df_prepro), columns=['proba_sans_pluie', 'proba_avec_pluie'])

# Concaténation de proba_pluie avec df_predi
df_predi = pd.concat([df_predi, proba_pluie], ignore_index=True)

# Insertion des prédictions dans la base de données au fur et à mesure qu'elles sont générées
insertion_sql(df_predi, db, cursor)

# Fermeture de la connexion à la base de données
fermeture_sql(db, cursor):
