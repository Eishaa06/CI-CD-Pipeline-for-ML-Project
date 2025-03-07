pipeline {
    agent any

    environment {
        // Keep your existing IDs/variables here:
        DOCKERHUB_CREDENTIALS = 'docker-hub-api-token'
        IMAGE_NAME = 'eishaa06/mlops-model'
        JENKINS_CONTAINER_NAME = "jenkins" // Optional if you don’t use it
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Eishaa06/CI-CD-Pipeline-for-ML-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
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
                body: """🚀 **Jenkins has completed the build!**
                - **Job Name:** ${JOB_NAME}
                - **Build Number:** ${BUILD_NUMBER}
                - **View Logs:** ${BUILD_URL}
                - **Docker Image:** \`${IMAGE_NAME}:latest\`
                🎉 Check your email for details.
                """
            )
        }
    }
}