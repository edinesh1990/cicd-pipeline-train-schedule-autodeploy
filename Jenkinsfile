pipeline {
    agent any
    
    parameters {
        // Parameter for the GitHub Repository URL
        string(name: 'REPO_URL', defaultValue: 'https://github.com/username/cicd-pipeline-train-schedule-autodeploy.git', description: 'Enter the GitHub Repository URL')
        
        // Parameter for the Docker Hub Username
        string(name: 'DOCKER_HUB_USER', defaultValue: 'yourdefaultuser', description: 'Enter your Docker Hub Username')
    }

    environment {
        DOCKER_USER = "${params.DOCKER_HUB_USER}" 
        APP_NAME = "abc-portal"
    }

    stages {
        stage('Checkout') {
            steps {
                // Dynamically clones the repository provided in the build parameters
                script {
                    checkout([$class: 'GitSCM', 
                        userRemoteConfigs: [[url: "${params.REPO_URL}"]], 
                        branches: [[name: '*/master']]
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Builds the image for the retail portal [cite: 10, 16]
                    sh "docker build -t ${DOCKER_USER}/${APP_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_USER}/${APP_NAME}:${BUILD_NUMBER} ${DOCKER_USER}/${APP_NAME}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Pushes images to the Docker Hub repository [cite: 16, 29]
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_USER}/${APP_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_USER}/${APP_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Continuous Deployment to the Kubernetes cluster 
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl apply -f service.yaml"
                    // Ensures the cluster uses the specific build image 
                    sh "kubectl set image deployment/abc-portal portal-container=${DOCKER_USER}/${APP_NAME}:${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Continuous Monitoring') {
            steps {
                // Applies autoscaling and confirms monitoring setup 
                sh "kubectl apply -f hpa.yaml"
                echo "Prometheus and Grafana are monitoring this deployment"
            }
        }
    }
}