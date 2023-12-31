import unittest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# Classe de test pour le modèle de machine learning
class TestMachineLearningModel(unittest.TestCase):

    # Test pour vérifier le chargement correct des données
    def test_data_loading(self):
        # Chemin vers le fichier de données
        chemin_fichier_donnees = os.path.join('data', 'data_features_with_location.csv')
        # Chargement des données
        df = pd.read_csv(chemin_fichier_donnees)
        # Vérifier que le DataFrame n'est pas None et n'est pas vide
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

    # Test pour vérifier l'entraînement correct du modèle
    def test_model_training(self):
        # Chargement des données
        df = pd.read_csv(os.path.join('data', 'data_features_with_location.csv'))
        # Encodage des variables catégorielles
        le = LabelEncoder()
        df['location_encoded'] = le.fit_transform(df['location'])
        # Préparation des données pour l'entraînement
        X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
        y = df['raintomorrow']
        # Séparation en ensembles d'entraînement et de test
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        # Entraînement du modèle
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        # Vérifier que le modèle n'est pas None après l'entraînement
        self.assertIsNotNone(model)

    # Test pour vérifier les prédictions du modèle
    def test_model_prediction(self):
        # Chargement des données
        df = pd.read_csv(os.path.join('data', 'data_features_with_location.csv'))
        # Encodage des variables catégorielles
        le = LabelEncoder()
        df['location_encoded'] = le.fit_transform(df['location'])
        # Préparation des données pour l'entraînement
        X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
        y = df['raintomorrow']
        # Séparation en ensembles d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Entraînement du modèle
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        # Faire des prédictions
        predictions = model.predict(X_test)
        # Vérifier que le nombre de prédictions correspond au nombre d'observations
        self.assertEqual(len(predictions), len(y_test))

# Exécute les tests si le script est exécuté directement
if __name__ == '__main__':
    unittest.main()
