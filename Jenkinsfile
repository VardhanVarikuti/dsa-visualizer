pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24.0.5-dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
    
    tty: true

  - name: jnlp
    image: jenkins/inbound-agent:latest
'''
        }
    }

    environment {
        DOCKER_HOST = 'tcp://127.0.0.1:2375'
        DOCKER_IMAGE = 'varikutivardhan/dsa-visualizer'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Info') {
            steps {
                container('docker') {
                    sh '''
                    echo "Waiting for Docker daemon..."
                    sleep 20

                    docker version
                    docker info
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    '''
                }
            }
        }

        stage('List Docker Images') {
            steps {
                container('docker') {
                    sh 'docker images'
                }
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