pipeline {
    agent any
    
    parameters {
        string(name: 'REPO_URL', defaultValue: 'https://github.com/edinesh1990/cicd-pipeline-train-schedule-autodeploy.git', description: 'GitHub Repository URL')
        string(name: 'DOCKER_HUB_USER', defaultValue: 'edinesh90', description: 'Docker Hub Username') 
    }

    environment {
        DOCKER_USER = "${params.DOCKER_HUB_USER}"
        APP_NAME = "abc-portal"
    }

    stages {
        stage('Checkout Source') {
            steps {
                // Clones the retail company's code [cite: 13]
                checkout([$class: 'GitSCM', 
                    userRemoteConfigs: [[url: "${params.REPO_URL}"]], 
                    branches: [[name: '*/feature/cicd-pipeline-project']]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                // Builds the image for the online shopping portal 
                bat "docker build -t %DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER% ."
                bat "docker tag %DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER% %DOCKER_USER%/%APP_NAME%:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Pushes images to the Docker-Hub repository [cite: 16, 29]
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    bat "echo %PASS% | docker login -u %USER% --password-stdin"
                    bat "docker push %DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER%"
                    bat "docker push %DOCKER_USER%/%APP_NAME%:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use the --kubeconfig flag to point to your actual config file
                // Replace 'YourUser' with your actual Windows username
                bat 'kubectl --kubeconfig="C:\\Users\\Lenovo\\.kube\\config" apply -f deployment.yaml'
                bat 'kubectl --kubeconfig="C:\\Users\\Lenovo\\.kube\\config" apply -f service.yaml'
                bat 'kubectl --kubeconfig="C:\\Users\\Lenovo\\.kube\\config" set image deployment/abc-portal portal-container=%DOCKER_USER%/%APP_NAME%:%BUILD_NUMBER%'
            }
        }

        stage('Monitoring & Scaling') {
            steps {
                // Sets up Autoscaling (HPA) and Continuous Monitoring [cite: 18, 31, 32]
                bat 'kubectl --kubeconfig="C:\\Users\\Lenovo\\.kube\\config"  kubectl apply -f hpa.yaml'
                echo "Deployment successful. Monitor via Prometheus/Grafana." 
            }
        }
    }
}
