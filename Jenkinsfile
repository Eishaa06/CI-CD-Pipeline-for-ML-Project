pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'docker-hub-api-token'  // Your existing credential ID
        IMAGE_NAME = "eishaa06/mlops-model"
        JENKINS_CONTAINER_NAME = "jenkins"    // Your container name
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Train Model') {
            steps {
                sh '''
                    apt-get update -y || true
                    apt-get install -y python3 python3-pip || true
                    python3 -m pip install -r requirements.txt || true
                    python3 model/train.py || true
                    python3 -m pytest tests/ || true
                '''
            }
        }

        stage('Commit Running Jenkins Container as Image') {
            steps {
                script {
                    sh '''
                        CONTAINER_ID=$(hostname)
                        docker commit $CONTAINER_ID ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Docker Push to DockerHub') {
            steps {
                script {
                    withCredentials([string(credentialsId: DOCKERHUB_CREDENTIALS, variable: 'DOCKERHUB_PAT')]) {
                        sh "echo ${DOCKERHUB_PAT} | docker login -u eishaa06 --password-stdin"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()  
            sh 'docker rmi ${IMAGE_NAME}:latest || true'
            sh 'docker logout || true'
        }
        
        success {
            emailext (
                subject: "Success: ML Model Deployment",
                body: "The ML model has been successfully deployed to Docker Hub.",
                to: "eishaharoon4@gmail.com",
                mimeType: 'text/html'
            )
        }
    }
}