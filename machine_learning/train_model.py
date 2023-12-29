import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Charger les données
df = pd.read_csv('data/data_features_with_location.csv')
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# Encodage des variables catégorielles
le = LabelEncoder()
df['location_encoded'] = le.fit_transform(df['location'])

# Préparation des données pour l'entraînement
X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
y = df['raintomorrow']

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Sauvegarde du modèle
joblib.dump(model, 'model.joblib')
