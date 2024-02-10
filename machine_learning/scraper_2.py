# Scrape Toutes les données des stations désirées pour la veille
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

import mysql.connector
from mysql.connector import Error

import pandas as pd
from datetime import datetime

import os 

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


def insertion_sql(data, db, cursor):

  """
    Insert les predictions dans une table MySQL.

    Parameters:
    - data: Probabilitees des predictions du modele.
    - db: Objet de connexion à la base de données.
    - cursor: Objet curseur pour exécuter des requêtes SQL.

  """

    nom_col = ['ville', 'day', 'Latitude', 'Longitude', 
               'temp_min', 'temp_max', 'rain', 'evap', 'sun', 'wind_dir', 'wind_speed', 
               '9am_temp', '9am_rh', '9am_cld', '9am_wind_dir', '9am_wind_speed', '9am_pression', 
               '3pm_temp', '3pm_rh', '3pm_cld', '3pm_wind_dir', '3pm_wind_speed', '3pm_pression']
    
    for i in range(len(data)):
        ville          = data.iloc[i]['ville'] 
        day            = data.iloc[i]['day'] 
        Latitude       = data.iloc[i]['Latitude']
        Longitude      = data.iloc[i]['Longitude'] 
        temp_min       = data.iloc[i]['temp_min'] 
        temp_max       = data.iloc[i]['temp_max'] 
        rain           = data.iloc[i]['rain'] 
        evap           = data.iloc[i]['evap']
        sun            = data.iloc[i]['sun']
        wind_dir       = data.iloc[i]['wind_dir']
        wind_speed     = data.iloc[i]['wind_speed']
        9am_temp       = data.iloc[i]['9am_temp'] 
        9am_rh         = data.iloc[i]['9am_rh'] 
        9am_cld        = data.iloc[i]['9am_cld']
        9am_wind_dir   = data.iloc[i]['9am_wind_dir'] 
        9am_wind_speed = data.iloc[i]['9am_wind_speed'] 
        9am_pression   = data.iloc[i]['9am_pression'] 
        3pm_temp       = data.iloc[i]['3pm_temp'] 
        3pm_rh         = data.iloc[i]['3pm_rh'] 
        3pm_cld        = data.iloc[i]['3pm_cld'] 
        3pm_wind_dir   = data.iloc[i]['3pm_wind_dir'] 
        3pm_wind_speed = data.iloc[i]['3pm_wind_speed'] 
        3pm_pression   = data.iloc[i]['3pm_pression']
        
    
        insert_query = ("INSERT INTO weather_scraped "
                        "(ville, day, Latitude, Longitude, temp_min, temp_max, rain, evap, sun, wind_dir, wind_speed, "
                        "9am_temp, 9am_rh, 9am_cld, 9am_wind_dir, 9am_wind_speed, 9am_pression, "
                        "3pm_temp, 3pm_rh, 3pm_cld, 3pm_wind_dir, 3pm_wind_speed, 3pm_pression) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        )
        cursor.execute(insert_query, (
                                    ville, day, Latitude, Longitude, temp_min, temp_max, rain, evap, sun, wind_dir, wind_speed, 
                                    9am_temp, 9am_rh, 9am_cld, 9am_wind_dir, 9am_wind_speed, 9am_pression, 
                                    3pm_temp, 3pm_rh, 3pm_cld, 3pm_wind_dir, 3pm_wind_speed, 3pm_pression
                                    )
                      )

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


def recuperation_param_pour_scrap():
    """
    Récupère les paramètres nécessaires pour le scraping à partir d'un fichier CSV.

    Returns:
        pd.DataFrame: DataFrame contenant des informations sur les stations à scraper.
    """
  
    # Chemin vers le fichier de données
    chemin_fichier_csv = os.path.join('data', 'data_for_scraping.csv')

    # Chargez le fichier CSV dans un DataFrame à remplacer par un appel à une table sql
    df_scrap = pd.read_csv(chemin_fichier_csv)

    return df_scrap

def scraping_veille(df_scrap):
    """
    Effectue le scraping des données météorologiques pour la veille.

    Args:
        df_scrap (pd.DataFrame): DataFrame contenant des informations sur les villes et les URL de scraping.

    Returns:
        pd.DataFrame: DataFrame contenant les données météorologiques extraites.
    """

    # Date du la veille
    date_format = "%Y%m%d"
    current_date = datetime.now().strftime(date_format)
  
    # Définitions des colonnes à scraper
    nom_col = ['ville', 'day', 'Latitude', 'Longitude', 
               'temp_min', 'temp_max', 'rain', 'evap', 'sun', 'wind_dir', 'wind_speed', 
               '9am_temp', '9am_rh', '9am_cld', '9am_wind_dir', '9am_wind_speed', '9am_pression', 
               '3pm_temp', '3pm_rh', '3pm_cld', '3pm_wind_dir', '3pm_wind_speed', '3pm_pression']
    
    num_col = [1, 2, 3, 4, 5, 6, 7, 
               9, 10, 11, 12, 13, 14, 
               15, 16, 17, 18, 19, 20]

    # Scraping
    list_data = []

    for i in range(len(df_scrap)):
        ville = df_scrap.loc[i, 'ville']
        Latitude = df_scrap.loc[i, 'Latitude']
        Longitude = df_scrap.loc[i, 'Longitude']
        id_url = df_scrap.loc[i, 'id_url']

        # URL => https://reg.bom.gov.au/climate/dwo/ + IDCJDWXXXX + .latest.shtml
        url = "".join(['https://reg.bom.gov.au/climate/dwo/', id_url, '.latest.shtml'])
    
        page = urlopen(url)
        soup = bs(page, "html.parser")
        ligne = soup.table.tbody.find_all('tr')[-1]

        data = [ville, current_date, Latitude, Longitude]
        colspan = 1
        colspan_val = ""
        colspan_done = 0
          
        for i, c in enumerate(num_col):
            if colspan > 1:
                data.append(colspan_val)
                colspan -= 1
                colspan_done += 1
                continue
                    
            if 'colspan' in ligne.find_all('td')[num_col[i - colspan_done]].attrs: 
                colspan = int(ligne.find_all('td')[num_col[i - colspan_done]].attrs['colspan'])
                data.append(colspan_val)
                continue
                    
            data.append(ligne.find_all('td')[num_col[i - colspan_done]].text.replace('\xa0', ''))
            
        list_data.append(data)


    dfs_list = [pd.DataFrame([dict(zip(nom_col, ligne))]) for ligne in list_data]

    # Concatène les DataFrames en un seul DataFrame
    last_day_data = pd.concat(dfs_list, ignore_index=True)

    return last_day_data

def save_data_scrapees(last_day_data):
    """
    Sauvegarde les données extraites dans une table sql.

    Args:
        last_day_data (pd.DataFrame): Le DataFrame contenant les données extraites.

    Returns:
        None
    """
  
    # Sauvegarde dans un fichier .csv à remplacer par une sauvegarde dans table sql
    #last_day_data.to_csv('data_scrapees_2.csv', index=False)

    # Connection à la base sql
    db, cursor = connection_base_sql()

    # Insertion des prédictions dans la base de données au fur et à mesure qu'elles sont générées
    insertion_sql(last_14_months_data, db, cursor)

    # Fermeture de la connexion à la base de données
    fermeture_sql(db, cursor):

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

# Processus de scraping des données de la veille
df_scrap = recuperation_param_pour_scrap()
last_day_data = scraping_veille(dates, df_scrap)
save_data_scrapees(last_day_data)
