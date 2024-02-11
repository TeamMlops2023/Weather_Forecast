# Weather_Forecast  

Notebook  
* Code de recherche pour le modèle ML utilisé.

Documentations
* Documentation et aide mis en place pour aider lors du développement du projet.
  
Les 3 dossiers ci-dessous s'organise en plusieurs partie comptant le code qui définie l'outil, le code pour le test, le code pour containeriser et enfin le code pour l'automatiser sur Jenkins.  
  
Database
* Rassemble le code permettant de définir, tester et automatiser tout ce qui concerne la définition de la base de donnée mysql.  
  
Fastapi  
* Rassemble le code permettant de définir, test et automatiser tout ce qui concerne la définition de l'api.  
  
Machine_learning  
* Rassemble le code permettant de définir, test et automatiser tout ce qui concerne la définition du modèle avec la récupération des données et leur préprocess.  
  
  
Kubernetes  
* Définition de l'architecture Kubernetes mise en place pour combiner l'ensemble des partie compossant l'application.  
  
Monitoring  
* Défini l'ensemble permettant de monitoré l'application dans son utilisation automatiser et définie sur kubernetes.

Airflow  
* Défini le code permettant de définir l'utilisation de Airflow dans le cadre de l'application (en développement).
  
Dockerfile  
* Définie le container pour installer le serveur Jenkins qui permettra l'automatisation de l'application.  

Docker-compose
* Fichier permettant des tests d'intégration directement via docker (en développement).
