#!/usr/bin/env bash

set -e

# Actualiza e instala herramientas necesarias
apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    software-properties-common \
    unixodbc-dev \
    gcc \
    g++ \
    make \
    python3-dev \
    python3-pip

# Agrega repositorio de Microsoft ODBC
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instala el driver ODBC 17
apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Actualiza pip y wheel antes de instalar dependencias
python3 -m pip install --upgrade pip wheel setuptools

# Instala las dependencias del proyecto
pip install -r requirements.txt
