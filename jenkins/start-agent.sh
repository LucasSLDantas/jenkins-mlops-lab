#!/bin/sh
set -eu

SECRET="$(tr -d '\r\n' < /run/secrets/agent-secret)"

if [ -z "$SECRET" ]; then
    echo "ERRO: segredo do agente está vazio."
    exit 1
fi

exec /usr/local/bin/jenkins-agent \
    -url "http://jenkins:8080/" \
    -name "mlops-agent" \
    -secret "$SECRET" \
    -webSocket \
    -workDir "/home/jenkins/agent"
