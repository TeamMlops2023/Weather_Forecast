# Utiliser l'image officielle de Jenkins avec JDK 11 comme base
FROM jenkins/jenkins:lts-jdk11

# Passer en utilisateur root pour installer Docker et Docker Compose
USER root

# Installer les prérequis
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# Installer Docker en utilisant le script d'installation rapide
RUN curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm get-docker.sh

# Installer Docker Compose en utilisant le lien direct vers la dernière version
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Installer kubectl
RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl

# Ajouter Docker Compose au PATH pour tous les utilisateurs (dans le profil global)
RUN echo 'PATH=$PATH:/usr/local/bin' >> /etc/profile

# Revenir à l'utilisateur Jenkins pour des raisons de sécurité
USER jenkins
