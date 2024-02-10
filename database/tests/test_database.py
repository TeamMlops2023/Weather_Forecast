import mysql.connector

# Connexion à la base de données
db = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="mlops",
    password="mlops",
    database="mlops_weather"
)

# Création de la table prediction (exemples simplifiés)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS weather_predictions (ville VARCHAR(100), date DATE, prediction VARCHAR(100), proba FLOAT, PRIMARY KEY (ville, date), CONSTRAINT unique_ville_date UNIQUE (ville, date));")
db.commit()

# Insertion de données de test (exemples simplifiés)
insert_query = "INSERT INTO weather_predictions (date, location, prediction, proba) VALUES (%s, %s, %s, %s)"
data = [
    ('Paris', '20160417', 'proba_sans_pluie', 0.87),
    ('Londre', '20160417', 'proba_avec_pluie', 0.90),
    ('Londre', '20160418', 'proba_sans_pluie', 0.60)
    # Ajoutez d'autres données ici
]

cursor.executemany(insert_query, data)
db.commit()


# Création de la table scraped(exemples simplifiés)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS weather_scraped  (ville VARCHAR(100), date DATE, Latitude FLOAT, Longitude FLOAT, temp_min FLOAT, temp_max FLOAT, rain FLOAT, evap FLOAT, sun FLOAT, wind_dir VARCHAR(3), wind_speed FLOAT, 9am_temp FLOAT, 9am_rh FLOAT, 9am_cld FLOAT,9am_wind_dir VARCHAR(3), 9am_wind_speed FLOAT, 9am_pression FLOAT, 3pm_temp FLOAT, 3pm_rh FLOAT, 3pm_cld FLOAT, 3pm_wind_dir VARCHAR(3), 3pm_wind_speed FLOAT, 3pm_pression FLOAT, PRIMARY KEY (ville, date), CONSTRAINT unique_ville_date UNIQUE (ville, date));")
db.commit()

# Insertion de données de test (exemples simplifiés)
insert_query = ("INSERT INTO weather_scraped "
                        "(ville, day, Latitude, Longitude, temp_min, temp_max, rain, evap, sun, wind_dir, wind_speed, "
                        "9am_temp, 9am_rh, 9am_cld, 9am_wind_dir, 9am_wind_speed, 9am_pression, "
                        "3pm_temp, 3pm_rh, 3pm_cld, 3pm_wind_dir, 3pm_wind_speed, 3pm_pression) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
               )
data = [
    ('Albury', '20221201', -36.07, 146.95, 14.4, 29.5, 0, 0, 0, 'NW', 35, 20.9, 75, 0, ' ', 0, 1003.7, 28.8, 24, 0, 'WSW', 19, 1001.2),
    ('Paris', '20221201', -36.07, 146.95, 14.4, 29.5, 0, 0, 0, 'NW', 35, 20.9, 75, 0, ' ', 0, 1003.7, 28.8, 24, 0, 'WSW', 19, 1001.2),
    ('Paris', '20221202', -36.07, 146.95, 14.4, 29.5, 0, 0, 0, 'NW', 35, 20.9, 75, 0, ' ', 0, 1003.7, 28.8, 24, 0, 'WSW', 19, 1001.2)
    # Ajoutez d'autres données ici
]

cursor.executemany(insert_query, data)
db.commit()

# Fermeture de la connexion
db.close()
