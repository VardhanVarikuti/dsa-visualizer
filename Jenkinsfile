pipeline {
    agent any

    environment {
        DOCKER_IMAGE    = 'varikutivardhan/dsa-visualizer'
        DOCKER_TAG      = "${BUILD_NUMBER}"
        DOCKER_CREDS_ID = 'dockerhub-credentials'
        KUBE_CONFIG     = credentials('kubeconfig')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "export KUBECONFIG=${KUBE_CONFIG} && kubectl apply -f kubernetes/"
                sh "export KUBECONFIG=${KUBE_CONFIG} && kubectl set image deployment/dsa-visualizer dsa-visualizer=${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }
    }

    post {
        always {
            sh "docker logout"
            cleanWs()
        }
    }
} 
