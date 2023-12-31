import mysql.connector

# Connexion à la base de données
db = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="mlops",
    password="mlops",
    database="mlops_weather"
)

# Création de la table (exemples simplifiés)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS weather_predictions (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, location VARCHAR(255), prediction INT, accuracy FLOAT)")
db.commit()

# Insertion de données de test (exemples simplifiés)
insert_query = "INSERT INTO weather_predictions (date, location, prediction, accuracy) VALUES (%s, %s, %s, %s)"
data = [
    ('2016-04-16', 'Norfolk Island', 0, 0.886467),
    ('2016-04-17', 'Norfolk Island', 0, 0.886467),
    # Ajoutez d'autres données ici
]

cursor.executemany(insert_query, data)
db.commit()

# Fermeture de la connexion
db.close()
