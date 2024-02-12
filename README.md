# Weather_Forecast  

Notebook  
* Code de recherche pour le modèle ML utilisé.  
  
Les 3 dossiers ci-dessous s'organisent en plusieurs parties comptant le code qui définit l'outil, le code pour le test, le code pour containeriser et enfin le code pour l'automatiser sur Jenkins.  
  
Database
* Rassemble le code permettant de définir, tester et automatiser tout ce qui concerne la définition de la base de donnée mysql.  
  
Fastapi  
* Rassemble le code permettant de définir, test et automatiser tout ce qui concerne la définition de l'api.  
  
Machine_learning  
* Rassemble le code permettant de définir, tester et automatiser tout ce qui concerne la définition du modèle avec la récupération des données et leur préprocess.  
  
  
Kubernetes  
* Définition de l'architecture Kubernetes mise en place pour combiner l'ensemble des parties compossant l'application.  
  
Monitoring  
* Définit l'ensemble permettant de monitorer l'application dans son utilisation automatisée et définie sur kubernetes.

Airflow  
* Définit le code permettant de définir l'utilisation de Airflow dans le cadre de l'application (en développement).
  
Dockerfile  
* Définit le container pour installer le serveur Jenkins qui permettra l'automatisation de l'application.  
