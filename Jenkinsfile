pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                sh "sudo apt install python3-pip"
            }
            steps{
                sh "pip install -r requirements"
            }       
        }
        stage('Test'){
            steps {
                sh "pytest"
            }
        }
        stage('Deploy'){
            steps {
                sh "echo 'Deployed'"
            }
        }
    }
}