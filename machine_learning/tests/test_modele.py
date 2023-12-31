import unittest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

class TestMachineLearningModel(unittest.TestCase):
    # Cette méthode est appelée avant chaque test. Elle prépare l'environnement de test.
    def setUp(self):
        # Chemin vers le fichier de données.
        chemin_fichier_donnees = os.path.join('data', 'data_features_with_location.csv')
        
        # Chargement des données depuis le fichier CSV.
        df = pd.read_csv(chemin_fichier_donnees)
        
        # Conversion de la date en format datetime.
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        
        # Encodage des variables catégorielles (ici, la localisation).
        le = LabelEncoder()
        df['location_encoded'] = le.fit_transform(df['location'])
        
        # Préparation des variables explicatives (X) et de la variable cible (y).
        self.X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
        self.y = df['raintomorrow']

    # Test pour vérifier le chargement correct des données.
    def test_data_loading(self):
        # Vérifie que les données ne sont pas vides.
        self.assertFalse(self.X.empty)
        self.assertFalse(self.y.empty)

    # Test pour vérifier l'entraînement correct du modèle.
    def test_model_training(self):
        # Séparation des données en ensembles d'entraînement et de test (ici, seul l'ensemble d'entraînement est utilisé).
        X_train, _, y_train, _ = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        
        # Création et entraînement du modèle.
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        # Vérification que le modèle a été bien entraîné et n'est pas vide.
        self.assertIsNotNone(model)

    # Test pour vérifier les prédictions du modèle.
    def test_model_prediction(self):
        # Séparation des données en ensembles d'entraînement et de test.
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        
        # Entraînement du modèle.
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        # Effectuer des prédictions sur l'ensemble de test.
        predictions = model.predict(X_test)
        
        # Vérification que le nombre de prédictions correspond au nombre de données de test.
        self.assertEqual(len(predictions), len(y_test))

if __name__ == '__main__':
    unittest.main()
