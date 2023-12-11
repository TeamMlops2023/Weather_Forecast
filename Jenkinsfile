pipeline {
    agent any

    environment {
        // Définir le nom de l'image Docker
        DOCKER_IMAGE = 'monapp/fastapi'
        // Définir le nom du conteneur
        CONTAINER_NAME = 'monapp-fastapi'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Cloner le dépôt GitHub
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Construire l'image Docker à partir du Dockerfile
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                // Supprimer le conteneur s'il existe déjà
                script {
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
                // Démarrer un nouveau conteneur à partir de l'image construite
                script {
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${DOCKER_IMAGE}"
                }
            }
        }
    }
    
    post {
        always {
            // Nettoyer les images Docker après la construction
            script {
                sh "docker rmi ${DOCKER_IMAGE} || true"
            }
        }
    }
}
