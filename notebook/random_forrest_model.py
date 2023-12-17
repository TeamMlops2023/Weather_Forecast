#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import numpy as pd
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
#from sklearn.metrics import confusion_matrix, roc_auc_score, ConfusionMatrixDisplay, precision_score, recall_score, f1_score, classification_report, roc_curve, auc, precision_recall_curve, average_precision_score
from sklearn.metrics import confusion_matrix, roc_auc_score, precision_score, recall_score, f1_score, classification_report, roc_curve, auc, precision_recall_curve, average_precision_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV, validation_curve
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression,f_classif,chi2

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


# In[5]:


import pandas as pd

df = pd.read_csv("data_features.csv", index_col=0)
df.head()


# In[6]:


# Séparation des données
# dataset optimisé
X = df.drop(['raintomorrow'],axis=1)
y = df['raintomorrow']

# Fractionnement des données 
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 10)


# In[7]:


# Taille des données d'entraînement et de test :

print("dataset optimisé :")
print("Length of Training Data: {}".format(len(X_train)))
print("Length of Testing Data: {}".format(len(X_test)))
print("\n")


# In[8]:


# Création du modèle de forêt aléatoire
random_forest_model = RandomForestClassifier(n_estimators=100, random_state=10)

# Entraînement du modèle avec les données d'entraînement
random_forest_model.fit(X_train, y_train)

# Prédiction sur les données de test
y_pred = random_forest_model.predict(X_test)

# Évaluation du modèle
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# In[ ]:




