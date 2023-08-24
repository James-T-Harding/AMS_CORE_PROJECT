pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                sh "sudo apt install -y python3-pip"
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test'){
            steps{
                echo 'Testing'
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deploying'
            }
        }
    }
}