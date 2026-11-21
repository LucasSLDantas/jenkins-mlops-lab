pipeline {
    agent none

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'ghcr.io/lucassldantas/jenkins-mlops-api'
        BUILDKIT_HOST = 'tcp://buildkit:1234'
    }

    stages {
        stage('CI - Testes e publicacao') {
            agent { label 'mlops' }

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
                        sh '.venv/bin/python -m pytest -v'
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

                                GHCR_AUTH="$(printf '%s:%s' "$GHCR_USER" "$GHCR_TOKEN" | base64 -w 0)"

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
        }

        stage('CD - Deploy') {
            agent { label 'deploy' }

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

                        IMAGE="${IMAGE_NAME}:${BUILD_NUMBER}"

                        printf '%s' "$GHCR_TOKEN" |
                            docker login ghcr.io \
                              -u "$GHCR_USER" \
                              --password-stdin

                        docker pull "$IMAGE"

                        docker rm -f jenkins-mlops-deploy 2>/dev/null || true

                        docker run -d \
                          --name jenkins-mlops-deploy \
                          --restart unless-stopped \
                          -p 127.0.0.1:8002:8000 \
                          "$IMAGE"

                        docker logout ghcr.io

                        echo "Deploy realizado: $IMAGE"
                    '''
                }
            }
        }

        stage('CD - Smoke Test') {
            agent { label 'deploy' }

            steps {
                sh '''
                    set -eu

                    for i in $(seq 1 15); do
                        if docker exec jenkins-mlops-deploy \
                            python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" ; then
                            echo "Smoke test aprovado!"
                            exit 0
                        fi

                        echo "Aguardando API iniciar..."
                        sleep 2
                    done

                    echo "ERRO: API nao respondeu ao health check."
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD concluido com sucesso!'
        }

        failure {
            echo 'Pipeline falhou. Consulte o Console Output.'
        }
    }
}
