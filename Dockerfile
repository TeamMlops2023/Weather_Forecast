FROM jenkins/jenkins:lts-jdk11

# Passer en utilisateur root pour installer les packages nécessaires
USER root

# Installer les prérequis
RUN apt-get update && apt-get install -y apt-transport-https \
   ca-certificates \
   curl \
   gnupg2 \
   software-properties-common

# Ajouter la clé GPG et le repository Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

# Installer Docker CLI et Docker Compose
RUN apt-get update && apt-get install -y docker-ce-cli \
    && curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Nettoyer les fichiers temporaires
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Ajouter Docker Compose au PATH (optionnel si déjà dans /usr/local/bin)
RUN echo 'PATH=$PATH:/usr/local/bin' >> /etc/profile

# Revenir à l'utilisateur Jenkins pour des raisons de sécurité
USER jenkins
