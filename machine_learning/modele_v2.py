import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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


def lecture_table_sql(db):
    # Création d'une requête SQL pour sélectionner toutes les colonnes de la table spécifiée
    query = "SELECT * FROM weather_scraped "

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
  - Ajout d'une colonne 'rain_tomorrow' initialisée à 0.
  - Itération sur chaque ville pour traiter les valeurs de 'rain'.
  - Suppression des lignes avec NaN.
  - Suppression des colonnes 'evap', 'sun', 'wind_dir', '9am_wind_dir', '3pm_wind_dir' pour simplifier le modèle
  - Séparation des variables cibles ('rain_tomorrow') et des features.

  Returns:
  - X: DataFrame des features.
  - y: Série des variables cibles 'rain_tomorrow'.
  """

  # Tri du DataFrame par 'ville' et 'day'
  df = df.sort_values(by=['ville', 'day'])

  # Réinitialisation des indices
  df = df.reset_index(drop=True)

  # Ajout d'une colonne 'rain_tomorrow' initialisée à 0
  df['rain_tomorrow'] = 0
  
  # DataFrame temporaire pour stocker les résultats
  df_b = pd.DataFrame(columns=df.columns)

  # Itération sur chaque ville pour traiter les valeurs de 'rain'
  for ville in df['ville'].value_counts().index:
      df_v = df.loc[df['ville']==ville]
    
      # Conversion des valeurs de 'rain' en 0 ou 1
      df_v['rain'] = df_v['rain'].apply(lambda x: 0 if x == '0' else 1)
    
      # Décalage des valeurs de 'rain' pour obtenir 'rain_tomorrow'
      df_v['rain_tomorrow'] = df_v['rain'].shift(-1)
    
      # Concaténation avec le DataFrame temporaire
      df_b = pd.concat([df_b, df_v], ignore_index=True)

  # Suppression de certaines colonnes pour simplifier le modèle dans le cadre du projet
  # 'evap', 'sun' sont souvent vides et 'wind_dir', '9am_wind_dir', '3pm_wind_dir' nécessitent un encodage particulier qu'on évite ici pour simplifier
  df_b = df_b.drop(['wind_dir', '9am_wind_dir', '3pm_wind_dir', 'evap', 'sun'], axis=1)
  
  # Suppression des lignes avec NaN
  df_train = df_b.dropna()
  
  # Séparation des variables cibles et des features
  X = df_train.drop(['rain_tomorrow', 'ville', 'day'], axis=1)
  y = df_train['rain_tomorrow']

  return df_b, X, y


def sauvegarde_modele(model):

  """
  Sauvegarde le modèle dans un fichier avec la date actuelle dans le nom du fichier.
  
  Args:
      model (object): L'objet du modèle à sauvegarder.

  Returns:
      None
  """

  # Obtenez la date actuelle au format 'YYYY-MM-DD'
  date_format = "%Y-%m-%d"
  current_date = datetime.now().strftime(date_format)

  # Construire le nom du fichier en ajoutant la date au modèle
  model_filename = f'model_{current_date}.pkl'

  # Chemin du nouveau fichier modèle
  chemin_fichier_model = os.path.join('data', model_filename)

  # Sauvegarde modèle
  joblib.dump(model, chemin_fichier_model)

  # Prédiction
  proba_pluie = pd.DataFrame(model.predict_proba(X), columns=['0', '1'])  # 0 pour sans_pluie et 1 pour avec_pluie.
  
################################################################################################################################################################################################################
################################################################################################################################################################################################################

# Connection à la base sql
db, cursor = connection_base_sql()

# Chemin vers le fichier de données
# chemin_fichier_donnees = os.path.join('data', 'data_scrapees_1.csv')

# Charger les données à partir de la table sql des données scrapees
# df = pd.read_csv(chemin_fichier_donnees)
df = lecture_table_sql(db)

# Préparation des données
data_propre, X, y = preparation_donne(df)

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Sauvegarde du modèle
sauvegarde_modele(model)

# Prédiction du modèle sur data_propre
X_predi = data_propre.drop(['rain_tomorrow', 'ville', 'day'], axis=1)
proba_pluie = pd.DataFrame(model.predict_proba(X_predi), columns=['proba_sans_pluie', 'proba_avec_pluie'])

# Ajout des probabilités de pluie à data_propre
data_propre = pd.concat([data_propre[['ville', 'day']], proba_pluie], axis=1)

# Insertion des prédictions dans la base de données au fur et à mesure qu'elles sont générées
insertion_sql(data_propre, db, cursor)

# Fermeture de la connexion à la base de données
fermeture_sql(db, cursor):
