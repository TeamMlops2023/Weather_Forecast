# Utiliser l'image officielle Jenkins LTS comme image de base
FROM jenkins/jenkins:lts

# (Optionnel) Installer des plugins Jenkins supplémentaires
# RUN /usr/local/bin/install-plugins.sh <liste-des-plugins>

# (Optionnel) Copier les fichiers de configuration personnalisés, les jobs, etc.
# COPY --chown=jenkins:jenkins config.xml /var/jenkins_home/config.xml
# COPY --chown=jenkins:jenkins jobs/ /var/jenkins_home/jobs/

# (Optionnel) Définir des variables d'environnement
# ENV JAVA_OPTS="-Xmx2048m"

#  Exposer les ports 
EXPOSE 8080 50000

# (Optionnel) Exécuter des scripts ou des commandes supplémentaires
USER root
RUN apt-get update && apt-get install -y 
USER jenkins

# Le point d'entrée est déjà défini dans l'image de base Jenkins, donc pas besoin de le redéfinir
