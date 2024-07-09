pipeline {
    agent any

    environment {
        registry = 'manasadev1/fastapi-app'
        registryCredential = 'Docker'
    }

    stages {
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
                    mkdir -p reports
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
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Remove Unused Docker Image') {
            steps {
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
