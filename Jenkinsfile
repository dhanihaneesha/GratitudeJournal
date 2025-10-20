pipeline {
    agent any

    environment {
        IMAGE_NAME = "dhanihaneesha/journal-app"
        IMAGE_TAG = "v${env.BUILD_NUMBER}"     // Automatically versioned using build number
    }

    stages {
        
        stage('Pull from SCM') {
            steps {
                echo "Pulling the latest code..."
                checkout scm   // Jenkins will pull the repo where the Jenkinsfile is stored
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub_creds', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    '''
                }
            }
        }

        stage('Push Docker Image to Dockerhub') {
            steps {
                echo "Pushing Docker image to Dockerhub..."
                bat "docker push %IMAGE_NAME%:%IMAGE_TAG%"
            }
        }

        stage('Update Kubernetes Deployment') {
            steps {
                echo "Updating image in Kubernetes Deployment manifest..."
                
                // Replace old image tag with new one
                bat """
                powershell -Command "(Get-Content deployment.yaml) `
                -replace 'image: .*', 'image: ${env.IMAGE_NAME}:${env.IMAGE_TAG}' `
                | Set-Content deployment.yaml"
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
            }
        }
    }

    post {
        success {
            echo "Deployment Successful!"
        }
        failure {
            echo "Deployment Failed!"
        }
    }
}
