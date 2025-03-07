pipeline {
    agent any
    
    parameters {
        string(name: 'DOCKER_HUB_USERNAME', defaultValue: 'eishaa06', description: 'Docker Hub username')
        password(name: 'DOCKER_HUB_TOKEN', defaultValue: '', description: 'Docker Hub API token or password')
    }
    
    environment {
        IMAGE_NAME = "${params.DOCKER_HUB_USERNAME}/mlops-model"
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
                    try {
                        // Try to use direct pip install
                        sh 'pip install --upgrade pip && pip install -r requirements.txt'
                    } catch (Exception e) {
                        // Fallback to Docker if direct install fails
                        echo "Using Docker for dependencies installation"
                        docker.image("python:3.9-slim").inside("-u root") {
                            sh 'python -m pip install --upgrade pip && python -m pip install -r requirements.txt'
                        }
                    }
                }
            }
        }
       
        stage('Train Model') {
            steps {
                script {
                    try {
                        // Try direct execution
                        sh 'python model/train.py'
                    } catch (Exception e) {
                        // Fallback to Docker
                        echo "Using Docker for model training"
                        docker.image("python:3.9-slim").inside("-u root") {
                            sh 'python model/train.py'
                        }
                    }
                }
            }
        }
       
        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Try direct execution
                        sh 'pytest tests/'
                    } catch (Exception e) {
                        // Fallback to Docker
                        echo "Using Docker for tests"
                        docker.image("python:3.9-slim").inside("-u root") {
                            sh 'pytest tests/'
                        }
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
                // Login using parameter token
                sh "echo ${params.DOCKER_HUB_TOKEN} | docker login -u ${params.DOCKER_HUB_USERNAME} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
       
        stage('Clean Up') {
            steps {
                // Add || true to prevent pipeline failure if cleanup fails
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
                sh "docker rmi ${IMAGE_NAME}:latest || true"
                sh "docker logout || true"
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
        
        always {
            echo "Pipeline completed with status: ${currentBuild.result}"
        }
    }
}