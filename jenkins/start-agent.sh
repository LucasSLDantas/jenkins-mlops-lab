#!/bin/sh
set -eu

export JENKINS_SECRET="$(tr -d '\r\n' < /run/secrets/agent-secret)"

if [ -z "$JENKINS_SECRET" ]; then
    echo "ERRO: segredo do agente está vazio."
    exit 1
fi

: "${JENKINS_URL:?JENKINS_URL nao configurada}"
: "${JENKINS_AGENT_NAME:?JENKINS_AGENT_NAME nao configurado}"

exec /usr/local/bin/jenkins-agent
