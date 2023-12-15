# Utilisez l'image officielle de Jenkins comme parent
FROM jenkins/jenkins:lts

# Passage en utilisateur root pour pouvoir installer des paquets
USER root

# Installation de Docker
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Installation de Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Revenir à l'utilisateur jenkins après l'installation
USER jenkins
