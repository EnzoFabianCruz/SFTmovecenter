#!/usr/bin/env bash
set -e

# Instala dependencias base
apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    software-properties-common \
    gcc \
    g++ \
    make

# Agrega la clave GPG y el repositorio de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Actualiza los repos y asegura instalación limpia de unixODBC y msodbcsql18
apt-get update

# Instala msodbcsql18 y unixODBC (el orden es importante para evitar conflictos)
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Verifica que el driver ODBC esté instalado correctamente
echo "Drivers ODBC instalados:"
odbcinst -q -d | grep -i "ODBC Driver"

# Instala pip y dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt
