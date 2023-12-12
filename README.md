### Weather_Forecast

# data
    - data_features_with_location.csv
        => contient les données nécessaires à l'entrainement du modèle.

# notebook
    - ... ====> Ce dossier serait intéressant pour isoler le code du modèle ML utilisé qu'on intègrera par la suite à app.py via import

# src
    - app.py 
        => Code python définisant l'application Fastapi et le modèle utilisé (création, entrainement et prédiction)
    - start_server.py
        => Code python exécutable qui sera utilisé pour lancer l'application Fastapi via uvicorn
    - requirements.txt
        => liste des packages nécessaire pour l'exécution du code de src.

# test
    - test_metrics.py
        => ...
    - test_run_model.py
        => ...
    - test.txt
        => ...

# monitoring
    - prometheus.yml
        => fichier déclaratif du bloc prométheus

# Docker
    - image-app
        => contient le dockerfile pour créer l'image du containers fastapi utilisé
    - docker-compose.yml
        => Fichier compose pour tester un ensemble de container en local

# Jenkins
    - Jenkinsfile
        => Fichier exécutable pour Jenkins
        
# contributeurs.txt
    => Fichir pour faire des test sur les commandes git/github

# process.txt
    => Fichier pour décrire le process et l'organisation du github