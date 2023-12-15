# Utilisez l'image Ubuntu 20.04 LTS comme base
FROM ubuntu:20.04

# Installez les dépendances
RUN apt-get update && \
    apt-get -y install apt-transport-https ca-certificates curl software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Créez l'utilisateur "jenkins"
RUN useradd -m -d /var/jenkins_home -s /bin/bash jenkins

# Ajoutez le référentiel Docker
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" && \
    apt-get update && \
    apt-get -y install docker-ce

# Ajoutez l'utilisateur "jenkins" au groupe "docker"
RUN usermod -aG docker jenkins

# Installez Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Revenez à l'utilisateur Jenkins
USER jenkins
