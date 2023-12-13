### Weather_Forecast

# notebook
    - ... ====> Ce dossier serait intéressant pour isoler le code du modèle ML utilisé qu'on intègrera par la suite à app.py via import

# code
    # fastapi1 :
        # data :
                - data_features_with_location.csv
                    => contient les données nécessaires à l'entrainement du modèle.
        # src :  
             - app.py 
                   => Code python définisant l'application Fastapi et le modèle utilisé (création, entrainement et prédiction)
               - start_server.py
                  => Code python exécutable qui sera utilisé pour lancer l'application Fastapi via uvicorn
               - requirements.txt
                   => liste des packages nécessaire pour l'exécution du code de src.
               - model_logs.log
                  => Fichier log créer par l'appel à fastapi /logs
               - setup_test_fastapi.sh
                  => fichier bash pour lancer toutes les commandes d'un coup pour pouvoir tester le bloc fastapi
              - setup_clean_fastapi.sh
                   => fichier bash pour lancer toutes les commandes d'un coup pour pouvoir nettoyer le bloc fastapi après phase de dev/test
              - commandes_test_fastapi.txt
                  => Listes des commandes pour tester fastapi de manière manuel (proto des blocs test à implémenter par la suite pour automatiser)
        # docker :
            - Dockerfile
    #  app2 :
        => anticipation d'une autre app
    - docker-compose.yml
        => Docker-compose pour faire les tests d'intégration sur un ensemble docker

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

# Jenkins
    - Jenkinsfile
        => Fichier exécutable pour Jenkins
        
# contributeurs.txt
    => Fichir pour faire des test sur les commandes git/github

# process.txt
    => Fichier pour décrire le process et l'organisation du github