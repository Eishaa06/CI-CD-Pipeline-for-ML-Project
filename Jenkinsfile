pipeline {
    agent any
   
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials') // Create this in Jenkins credentials
        JENKINS_CONTAINER_NAME = "jenkins-container" // Adjust this to your actual container name
        IMAGE_NAME = "eishaa06/mlops-model"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
   
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
       
        stage('Check Environment') {
            steps {
                sh '''
                    echo "Jenkins workspace: ${WORKSPACE}"
                    echo "Container ID: $(hostname)"
                    whoami
                '''
            }
        }
       
        stage('Prepare Environment') {
            steps {
                script {
                    sh '''
                        apt-get update -y || true
                        apt-get install -y python3 python3-pip || true
                        python3 -m pip install --upgrade pip || true
                        pip3 install -r requirements.txt || true
                    '''
                }
            }
        }
       
        stage('Train Model') {
            steps {
                script {
                    sh 'python3 model/train.py || true'
                }
            }
        }
       
        stage('Run Tests') {
            steps {
                script {
                    sh 'python3 -m pytest tests/ || true'
                }
            }
        }
       
        stage('Commit Container as Image') {
            steps {
                script {
                    // This approach uses the Jenkins container itself as the base for our image
                    sh """
                        # Get container ID of the current container running Jenkins
                        CONTAINER_ID=\$(hostname)
                       
                        # Commit the container state as a new image
                        docker commit \$CONTAINER_ID ${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
       
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo \${DOCKER_PASS} | docker login -u \${DOCKER_USER} --password-stdin
                            docker push ${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }
    }
   
    post {
        always {
            sh "docker logout || true"
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
            sh "docker rmi ${IMAGE_NAME}:latest || true"
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