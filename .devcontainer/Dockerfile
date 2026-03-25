FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Azure CLI と必須パッケージをインストール
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        apt-transport-https \
        lsb-release \
        gnupg \
    && curl -sLS https://packages.microsoft.com/keys/microsoft.asc \
        | gpg --dearmor \
        | tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null \
    && AZ_REPO=$(lsb_release -cs) \
    && echo "deb [arch=$(dpkg --print-architecture)] https://packages.microsoft.com/repos/azure-cli/ ${AZ_REPO} main" \
        > /etc/apt/sources.list.d/azure-cli.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends azure-cli \
    && rm -rf /var/lib/apt/lists/*

# Azure Developer CLI (azd) をインストール
RUN curl -fsSL https://aka.ms/install-azd.sh | bash
