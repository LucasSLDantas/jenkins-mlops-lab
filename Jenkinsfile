pipeline {
    agent { label 'mlops' }

    options {
        timestamps()
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
                      --addr tcp://buildkit:1234 \
                      build \
                      --frontend dockerfile.v0 \
                      --local context=. \
                      --local dockerfile=. \
                      --output type=oci,dest=/tmp/jenkins-mlops-api.tar
                '''
            }
        }
    }

    post {
        success {
            echo 'CI concluido: testes e Docker Build executados!'
        }

        failure {
            echo 'Pipeline falhou: verifique o console do Jenkins.'
        }
    }
}
