pipeline {
    agent any
    
    // Corrected block: Parameters must be wrapped in a 'parameters' block
    parameters {
        string(name: 'REPO_URL', defaultValue: 'https://github.com/bhavukm/cicd-pipeline-train-schedule-autodeploy', description: 'GitHub Repository URL') [cite: 35]
        string(name: 'DOCKER_HUB_USER', defaultValue: 'edinesh90', description: 'Docker Hub Username') [cite: 29]
    }

    environment {
        // Path to your local Docker and Kubernetes binaries
        PATH = "C:\\Program Files\\Docker\\Docker\\resources\\bin;${env.PATH}"
        DOCKER_USER = "${params.DOCKER_HUB_USER}"
        APP_NAME = "abc-portal"
    }

    stages {
        stage('Checkout Source') {
            steps {
                // Clones the source code repository [cite: 13, 21]
                checkout([$class: 'GitSCM', 
                    userRemoteConfigs: [[url: "${params.REPO_URL}"]], 
                    branches: [[name: '*/master']]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                // Builds the Docker image using Windows Batch [cite: 16]
                bat "docker build -t %DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER% ."
                bat "docker tag %DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER% %DOCKER_USER%/%APP_NAME%:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Pushes the built image to Docker Hub repository [cite: 16, 29]
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    bat "echo %PASS% | docker login -u %USER% --password-stdin"
                    bat "docker push %DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER%"
                    bat "docker push %DOCKER_USER%/%APP_NAME%:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Continuous Deployment to local Kubernetes cluster [cite: 17, 30, 33]
                bat "kubectl apply -f deployment.yaml"
                bat "kubectl apply -f service.yaml"
                // Updates the container with the new feature image [cite: 11, 15]
                bat "kubectl set image deployment/abstergo-portal portal-container=%DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER%"
            }
        }

        stage('Continuous Monitoring') {
            steps {
                // Triggers autoscaling and ensures continuous monitoring is active [cite: 18, 31, 32]
                bat "kubectl apply -f hpa.yaml"
                echo "Prometheus and Grafana are monitoring this deployment." [cite: 24, 26]
            }
        }
    }
}
