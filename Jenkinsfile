pipeline {
    agent any
    environment {
        // Use an API token stored as a Jenkins credential
        //DOCKER_HUB_TOKEN = "${params.DOCKER_HUB_TOKEN}"
        DOCKER_HUB_TOKEN = credentials('dckr_pat_93JkqvM9z_GclmS7hEM_Qz28eyM')
        DOCKER_HUB_USERNAME = 'eishaa06'  // Replace with your actual username
        IMAGE_NAME = "${DOCKER_HUB_USERNAME}/mlops-model"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
       
        stage('Install Dependencies') {
            steps {
                script {
                    docker.image("python:3.9-slim").inside("-u root") {
                        sh 'python -m pip install --upgrade pip && python -m pip install -r requirements.txt'
                    }
                }
            }
        }
       
        stage('Train Model') {
            steps {
                script {
                    docker.image("python:3.9-slim").inside("-u root") {
                        sh 'python model/train.py'
                    }
                }
            }
        }
       
        stage('Run Tests') {
            steps {
                script {
                    docker.image("python:3.9-slim").inside("-u root") {
                        sh 'pytest tests/'
                    }
                }
            }
        }
       
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }
       
        stage('Push to Docker Hub') {
            steps {
                // Login using API token
                sh "echo ${DOCKER_HUB_TOKEN} | docker login -u ${DOCKER_HUB_USERNAME} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
       
        stage('Clean Up') {
            steps {
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker rmi ${IMAGE_NAME}:latest"
                sh "docker logout"
            }
        }
    }
   
    post {
        success {
            emailext (
                subject: "Success: ML Model Deployment - Build #${env.BUILD_NUMBER}",
                body: """
                <p>The ML model has been successfully deployed.</p>
                <p><b>Build:</b> ${env.BUILD_NUMBER}</p>
                <p><b>Docker Image:</b> ${IMAGE_NAME}:${IMAGE_TAG}</p>
                <p>Check the <a href='${env.BUILD_URL}'>Jenkins build</a> for more details.</p>
                """,
                to: "eishaharoon4@gmail.com",
                mimeType: 'text/html'
            )
        }
       
        failure {
            emailext (
                subject: "Failed: ML Model Deployment - Build #${env.BUILD_NUMBER}",
                body: """
                <p>The ML model deployment has failed.</p>
                <p><b>Build:</b> ${env.BUILD_NUMBER}</p>
                <p>Check the <a href='${env.BUILD_URL}'>Jenkins build</a> for more details.</p>
                """,
                to: "eishaharoon4@gmail.com",
                mimeType: 'text/html'
            )
        }
    }
}