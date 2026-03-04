pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        // Tera Docker Hub Username
        IMAGE_NAME = "harry1290/multibranch-flask-app"
        // Tera GitHub Username aur Email
        GIT_USER   = "HariomChoudhary1290" 
        GIT_EMAIL  = "hariom.choudhary015@gmail.com"
    }

    stages {
        stage('Checkout') {
            steps {
                // SCM se code checkout karega
                checkout scm
            }
        }

        stage('Build and Push Image') {
            when { branch 'main' }
            steps {
                script {
                    env.IMAGE_TAG = "build-${BUILD_NUMBER}"

                    // Jenkins me ID 'docker-creds' rakhna
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Update K8s Manifest') {
            when { branch 'main' }
            steps {
                script {
                    // Jenkins me ID 'github-creds' rakhna
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

                        # Deployment file mein image tag update karega
                        sed -i "s|image:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|" k8s/deployment.yml

                        git add k8s/deployment.yml
                        git diff --cached --quiet || git commit -m "Updated image to ${IMAGE_TAG}"
                        
                        # Tera Token aur sahi Repo URL
                        git push https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/HariomChoudhary1290/Multi-Branch-Prod.git main
                        """
                    }
                }
            }
        }
    }
}