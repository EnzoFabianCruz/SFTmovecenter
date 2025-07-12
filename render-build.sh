#!/usr/bin/env bash
set -e

# Instala dependencias
apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    software-properties-common \
    unixodbc-dev \
    gcc \
    g++ \
    make

# Agrega repositorio de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Actualiza e instala driver ODBC 18
apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Instala dependencias de Python
pip install -r requirements.txt
