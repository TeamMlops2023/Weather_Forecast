import unittest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

class TestMachineLearningModel(unittest.TestCase):

    def setUp(self):
        chemin_fichier_donnees = os.path.join('data', 'data_features_with_location.csv')
        df = pd.read_csv(chemin_fichier_donnees)
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        le = LabelEncoder()
        df['location_encoded'] = le.fit_transform(df['location'])
        self.X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
        self.y = df['raintomorrow']

    def test_data_loading(self):
        self.assertFalse(self.X.empty)
        self.assertFalse(self.y.empty)

    def test_model_training(self):
        X_train, _, y_train, _ = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        self.assertIsNotNone(model)

    def test_model_prediction(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        self.assertEqual(len(predictions), len(y_test))

if __name__ == '__main__':
    unittest.main()
