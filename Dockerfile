FROM python:3.10-slim

# Evita preguntas interactivas
ENV DEBIAN_FRONTEND=noninteractive

# Instala herramientas y dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    software-properties-common \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    libgssapi-krb5-2 \
    make \
    && rm -rf /var/lib/apt/lists/*

# Agrega claves y repositorio de Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN odbcinst -i -d -f /etc/odbcinst.ini
# Copia los archivos de la app
WORKDIR /app
COPY . /app

# Instala dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto 8000 (por defecto en gunicorn)
EXPOSE 8000

# Comando para iniciar la app con gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
