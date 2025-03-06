pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDS = credentials('docker-hub-credentials')
        IMAGE_NAME = 'yourusername/mlops-model'  // Replace with your Docker Hub username
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
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Train Model') {
            steps {
                sh 'python model/train.py'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
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
                sh "echo $DOCKER_HUB_CREDS_PSW | docker login -u $DOCKER_HUB_CREDS_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
        
        stage('Clean Up') {
            steps {
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker rmi ${IMAGE_NAME}:latest"
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
                to: "admin@example.com", // Replace with admin email
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
                to: "admin@example.com", // Replace with admin email
                mimeType: 'text/html'
            )
        }
    }
}