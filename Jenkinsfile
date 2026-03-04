pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "harry1290/multibranch-flask-app"
        GIT_USER   = "HariomChoudhary1290"
        GIT_EMAIL  = "hariom.choudhary015@gmail.com"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push Docker Image') {
            when { branch 'main' }
            steps {
                script {

                    env.IMAGE_TAG = "build-${BUILD_NUMBER}"

                    withCredentials([usernamePassword(
                        credentialsId: 'docker-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {

                        sh """
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Update Kubernetes Manifest') {
            when { branch 'main' }
            steps {
                script {

                    withCredentials([usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_TOKEN'
                    )]) {

                        sh """
                        set -e

                        git config user.name "${GIT_USER}"
                        git config user.email "${GIT_EMAIL}"

                        git fetch origin
                        git checkout main
                        git reset --hard origin/main

                        # Update image tag in deployment
                        sed -i "s|image: .*|image: ${IMAGE_NAME}:${IMAGE_TAG}|" k8s/deployment.yml

                        git add k8s/deployment.yml

                        git diff --cached --quiet || git commit -m "Update image to ${IMAGE_TAG}"

                        git remote set-url origin https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/HariomChoudhary1290/Multi-Branch-Prod.git

                        git push origin main
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Build and deployment completed successfully 🚀"
        }
        failure {
            echo "Pipeline failed ❌"
        }
    }
}