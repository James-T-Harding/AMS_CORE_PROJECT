pipeline {
    agent any
    stages {
        stage('Build'){
            sh "pip install -r requirements"
        }
        stage('Test'){
            sh "pytest"
        }
        stage('Deploy'){
            sh "echo 'Deployed'"
        }
    }
}