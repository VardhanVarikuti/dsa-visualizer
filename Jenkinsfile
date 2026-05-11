pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'varikutivardhan/dsa-visualizer'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Project Info') {
            steps {
                sh '''
                echo "Listing project files..."
                ls -la
                '''
            }
        }

        stage('Validate Kubernetes Files') {
            steps {
                sh '''
                echo "Checking Kubernetes manifests..."
                ls kubernetes
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                echo "Building Docker image..."
                docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                '''
            }
        }

        stage('Docker Images') {
            steps {
                sh '''
                docker images
                '''
            }
        }

        stage('Pipeline Complete') {
            steps {
                echo 'DSA Visualizer CI/CD pipeline executed successfully!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS'
        }

        failure {
            echo 'Pipeline FAILED'
        }
    }
}