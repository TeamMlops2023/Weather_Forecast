pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build and Deploy') {
            steps {
                sh 'docker-compose -f deployment/docker-compose.yml build'
                sh 'docker-compose -f deployment/docker-compose.yml up -d'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'echo "Running tests..."'
                // Exécutez ici vos scripts de test
            }
        }
    }
    
    post {
        always {
            sh 'docker-compose -f deployment/docker-compose.yml down'
            echo 'Cleaning up...'
        }
    }
}
