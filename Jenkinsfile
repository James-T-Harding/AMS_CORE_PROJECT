pipeline {
    agent any
    environment {
        SECRET_KEY=credentials('SECRET_KEY')
    }
    stages {
        stage('Build'){
            steps{
                sh "echo 'Building...'"
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