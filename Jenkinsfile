pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"   // ✅ Set your AWS region
        DOCKER_IMAGE = "my-python-app:${BUILD_NUMBER}"
        CONTAINER_NAME = "my-python-app"
        TF_DIR = "tf.project"        // ✅ path where terraform files exist
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/shubham101314/practice-repo-13.git'   // ✅ FIX: add repo URL
            }
        }

        stage('Get ECR Repo from Terraform') {
            steps {
                dir("${TF_DIR}") {
                    script {
                        ECR_REPO = sh(
                            script: "terraform output -raw ecr_repo_url",
                            returnStdout: true
                        ).trim()
                    }
                }
                echo "Using ECR Repository: ${ECR_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Tag Docker Image for ECR') {
            steps {
                script {
                    sh """
                    docker tag ${DOCKER_IMAGE} ${ECR_REPO}:${BUILD_NUMBER}
                    docker tag ${DOCKER_IMAGE} ${ECR_REPO}:latest
                    """
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO}
                    """
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    sh """
                    docker push ${ECR_REPO}:${BUILD_NUMBER}
                    docker push ${ECR_REPO}:latest
                    """
                }
            }
        }

        stage('Deploy Container Locally') {
            steps {
                script {
                    sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      --restart unless-stopped \
                      -p 5000:5000 \
                      ${ECR_REPO}:latest
                    """
                }
            }
        }

        stage('Cleanup Old Images (Optional)') {
            steps {
                script {
                    sh """
                    REPO_NAME=\$(basename ${ECR_REPO})

                    aws ecr describe-images \
                      --repository-name \$REPO_NAME \
                      --region ${AWS_REGION} \
                      --query 'sort_by(imageDetails,&imagePushedAt)[].imageDigest' \
                      --output text > all_digests.txt

                    total=\$(wc -l < all_digests.txt)

                    if [ "\$total" -gt 10 ]; then
                      old_digests=\$(head -n \$((total-10)) all_digests.txt)
                      for digest in \$old_digests; do
                        aws ecr batch-delete-image \
                          --repository-name \$REPO_NAME \
                          --region ${AWS_REGION} \
                          --image-ids imageDigest=\$digest
                      done
                    fi
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline executed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
        always {
            cleanWs()
        }
    }
}