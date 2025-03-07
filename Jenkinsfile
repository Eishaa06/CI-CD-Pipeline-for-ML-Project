pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Eishaa06/CI-CD-Pipeline-for-ML-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t eishaa06/mymlapp .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-api-token', url: '']) {
                    sh 'docker tag eishaa06/mymlapp eishaa06/mymlapp:latest'
                    sh 'docker push eishaa06/mymlapp:latest'
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
                to: 'eishaharoon4@gmail.com',
                subject: "✅ Jenkins Build: ${JOB_NAME} #${BUILD_NUMBER}",
                body: """🚀 **Jenkins has completed the build!**
                - **Job Name:** ${JOB_NAME}
                - **Build Number:** ${BUILD_NUMBER}
                - **View Logs:** ${BUILD_URL}
                - **Docker Image:** \`eishaa06/mymlapp:latest\`
                🎉 Check your email for details.
                """
            )
        }
    }
}