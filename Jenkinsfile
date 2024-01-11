pipeline {
    agent any
    environment {
        KUBECONFIG = '/var/jenkins_home/.kube/config'
    }
    stages {
        stage('Execute Jenkinsfile_fastapi') {
            steps {
                script {
                    load 'fastapi/Jenkinsfile_fastapi'
                }
            }
        }
        stage('Pause After FastAPI') {
            steps {
                script {
                    sleep 30
                }
            }
        }
        stage('Execute Jenkinsfile_SQL') {
            steps {
                script {
                    load 'database/Jenkinsfile_SQL'
                }
            }
        }
        stage('Pause After SQL') {
            steps {
                script {
                    sleep 30
                }
            }
        }
        stage('Execute Jenkinsfile_ML') {
            steps {
                script {
                    load 'machine_learning/Jenkinsfile_ML'
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
