pipeline {
    agent any
    environment {
        KUBECONFIG = '/var/jenkins_home/.kube/config'
    }
    stages {
        stage('Execute Jenkinsfile_fastapi') {
            steps {
                script {
                    // Charger et exécuter Jenkinsfile_fastapi
                    load 'Weather_Forecast/fastapi/Jenkinsfile_fastapi'
                }
            }
        }
        stage('Pause') {
            steps {
                script {
                    // Pause de 30 secondes
                    sleep 30
                }
            }
        }
        stage('Execute Jenkinsfile_SQL') {
            steps {
                script {
                    // Charger et exécuter Jenkinsfile_SQL
                    load 'Weather_Forecast/database/Jenkinsfile_SQL'
                }
            }
        }
        stage('Pause') {
            steps {
                script {
                    // Pause de 30 secondes
                    sleep 30
                }
            }
        }
        stage('Execute Jenkinsfile_ML') {
            steps {
                script {
                    // Charger et exécuter Jenkinsfile_ML
                    load 'Weather_Forecast/machine_learning/Jenkinsfile_ML'
                }
            }
        }
    }
    post {
        always {
            echo 'Orchestration des pipelines terminée. Vérifiez les logs pour les détails.'
        }
    }
}
