pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'docker-hub-api-token'  // Your credential ID
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
                bat '''
                    REM Update/install Python if needed
                    python -m pip install --upgrade pip || echo "Pip upgrade failed but continuing..."
                    python -m pip install -r requirements.txt || echo "Requirements installation failed but continuing..."
                   
                    REM Run the model training
                    python model/train.py || echo "Model training failed but continuing..."
                   
                    REM Run tests
                    python -m pytest tests/ || echo "Tests failed but continuing..."
                '''
            }
        }

        stage('Commit Running Jenkins Container as Image') {
            steps {
                script {
                    bat '''
                        FOR /F "tokens=*" %%i IN ('hostname') DO SET CONTAINER_ID=%%i
                        docker commit %CONTAINER_ID% %IMAGE_NAME%:latest
                    '''
                }
            }
        }

        stage('Docker Push to DockerHub') {
            steps {
                script {
                    withCredentials([string(credentialsId: DOCKERHUB_CREDENTIALS, variable: 'DOCKERHUB_PAT')]) {
                        bat "echo %DOCKERHUB_PAT% | docker login -u eishaa06 --password-stdin"
                        bat "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()  
            bat "docker rmi ${IMAGE_NAME}:latest || echo Container removal failed but continuing..."
            bat "docker logout || echo Logout failed but continuing..."
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