#!/usr/bin/env bash

set -e

apt-get update && apt-get install -y curl gnupg2 apt-transport-https software-properties-common unixodbc-dev

# Repositorio de Microsoft para ODBC
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Instalar las dependencias Python
pip install -r requirements.txt

# Verificar que el driver fue instalado
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"