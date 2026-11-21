pipeline {
    agent { label 'mlops' }

    options {
        timestamps()
    }

    environment {
        IMAGE_NAME = 'ghcr.io/lucassldantas/jenkins-mlops-api'
        BUILDKIT_HOST = 'tcp://buildkit:1234'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Preparar ambiente Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Testes automatizados') {
            steps {
                sh '''
                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    buildctl \
                      --addr "$BUILDKIT_HOST" \
                      build \
                      --frontend dockerfile.v0 \
                      --local context=. \
                      --local dockerfile=. \
                      --output type=oci,dest=/tmp/jenkins-mlops-api.tar
                '''
            }
        }

        stage('Publicar no GHCR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-credentials',
                        usernameVariable: 'GHCR_USER',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        set -eu

                        export DOCKER_CONFIG="$(mktemp -d)"
                        chmod 700 "$DOCKER_CONFIG"

                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        export GHCR_AUTH="$(printf '%s:%s' "$GHCR_USER" "$GHCR_TOKEN" | base64 -w 0)"

                        printf '{"auths":{"ghcr.io":{"auth":"%s"}}}\\n' \
                            "$GHCR_AUTH" > "$DOCKER_CONFIG/config.json"

                        chmod 600 "$DOCKER_CONFIG/config.json"
                        unset GHCR_AUTH

                        buildctl \
                          --addr "$BUILDKIT_HOST" \
                          build \
                          --frontend dockerfile.v0 \
                          --local context=. \
                          --local dockerfile=. \
                          --output "type=image,name=${IMAGE_NAME}:${BUILD_NUMBER},push=true"

                        echo "Imagem publicada: ${IMAGE_NAME}:${BUILD_NUMBER}"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline concluido: testes, build e publicacao executados!'
        }

        failure {
            echo 'Pipeline falhou: verifique o console do Jenkins.'
        }
    }
}
