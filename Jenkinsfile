pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                sh "sudo apt install -y python3-pip python3-pytest"
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test'){
            steps{
                sh "pytest"
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deploying'
            }
        }
    }
}