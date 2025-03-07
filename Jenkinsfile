pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'docker-hub-api-token'
        IMAGE_NAME = 'eishaa06/mlops-model'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Eishaa06/CI-CD-Pipeline-for-ML-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Checking Docker installation..."
                    sh "docker --version" // Debugging Docker installation
                }
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: DOCKERHUB_CREDENTIALS, url: '']) {
                    sh "docker tag ${IMAGE_NAME} ${IMAGE_NAME}:latest"
                    sh "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "🔔 Sending email notification..."
            }
            emailext(
                to: "eishaharoon4@gmail.com",
                subject: "✅ Jenkins Build: ${JOB_NAME} #${BUILD_NUMBER}",
                body: """<p>🚀 Jenkins has completed the build!</p>
                <ul>
                  <li><b>Job Name:</b> ${JOB_NAME}</li>
                  <li><b>Build Number:</b> ${BUILD_NUMBER}</li>
                  <li><b>View Logs:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></li>
                  <li><b>Docker Image:</b> ${IMAGE_NAME}:latest</li>
                </ul>
                🎉 Check your email for details.
                """,
                mimeType: 'text/html'
            )
        }
    }
}
