pipeline {
    agent {
        docker {
            image 'python:3.9-slim' // Use a lightweight Python Docker image with Docker CLI pre-installed
            args '-v /var/run/docker.sock:/var/run/docker.sock' // Mount Docker socket
        }
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-api-token') // Configure in Jenkins
        IMAGE_NAME = "eishaa06/mlops-model"
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
                sh '''
                    apt-get update -y
                    apt-get install -y python3-pip
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh 'python3 model/train.py'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-api-token',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                docker logout || true
                docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                docker rmi ${IMAGE_NAME}:latest || true
            '''
            cleanWs()
        }

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
