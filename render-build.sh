#!/usr/bin/env bash

set -e

# Actualiza paquetes y dependencias necesarias
apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    software-properties-common \
    unixodbc-dev \
    gcc \
    g++ \
    make

# Agrega la clave y el repo de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Actualiza y fuerza la instalación del driver ODBC 17
apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Verifica que esté instalado correctamente
echo "Verificando instalación del driver..."
odbcinst -q -d | grep -i "ODBC Driver 17"

# Instala dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt
