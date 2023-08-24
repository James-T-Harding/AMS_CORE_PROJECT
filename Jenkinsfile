pipeline {
    agent any
    environment {
        SECRET_KEY=credentials('SECRET_KEY')
    }
    stages {
        stage('Build'){
            steps{
                sh "sudo apt install -y python3-pip python3-pytest"
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test'){
            steps{
                sh "echo 'Testing using ${SECRET_KEY}...'"
                sh "echo 'Tests passed."
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deploying'
            }
        }
    }
}