pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Cloner le dépôt GitHub
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                // Exécuter un script de test fictif ou une commande
                // Remplacez ceci par la commande que vous souhaitez exécuter
                sh 'echo "Running tests..."'
                // Par exemple, si vous avez un script de test :
                // sh './run-tests.sh'
            }
        }
    }
    
    post {
        always {
            // Mettez ici les étapes de nettoyage si nécessaire
            echo 'Cleaning up...'
        }
    }
}
