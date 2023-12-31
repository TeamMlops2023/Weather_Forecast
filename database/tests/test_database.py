# -*- coding: utf-8 -*-
import unittest
import mysql.connector

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connexion à la base de données
        cls.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysecretpassword',
            database='mlops_weather'
        )
        cls.cursor = cls.db.cursor()

        # Création de la table et insertion des données
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_predictions (
                id INT PRIMARY KEY,
                date DATE,
                location VARCHAR(255),
                prediction INT,
                accuracy FLOAT
            );
        """)
        cls.cursor.execute("""
            INSERT INTO weather_predictions (id, date, location, prediction, accuracy) VALUES
                (41053, '2016-04-16', 'Norfolk Island', 0, 0.886467),
                (41054, '2017-05-08', 'Sydney', 1, 0.886467);
        """)
        cls.db.commit()

    def test_weather_predictions_table_exists(self):
        """Vérifie si la table weather_predictions existe."""
        self.cursor.execute("SHOW TABLES LIKE 'weather_predictions'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_inserted_data(self):
        """Vérifie si les données sont insérées correctement."""
        self.cursor.execute("SELECT * FROM weather_predictions WHERE id=41053")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.db.close()

if __name__ == '__main__':
    unittest.main()
