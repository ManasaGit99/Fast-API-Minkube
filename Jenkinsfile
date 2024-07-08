pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('Docker')  // Update with your Docker Hub credentials ID
        DOCKERHUB_IMAGE = 'manasadev1/fastapi-app'  // Update with your Docker Hub username and image name
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ManasaGit99/Fast-API-Minkube.git'  // Update with your GitHub repo URL
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install fastapi uvicorn kubernetes requests pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest --junitxml=reports/results.xml
                '''
            }
            post {
                always {
                    junit 'reports/results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${env.DOCKERHUB_IMAGE}:${env.BUILD_NUMBER}", "-f Dockerfile .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', env.DOCKERHUB_CREDENTIALS) {
                        dockerImage.push()
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
