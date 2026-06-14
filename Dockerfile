FROM python:3.12-slim

WORKDIR /app

# Instaluj zależności systemowe potrzebne przez psycopg2 i ortools
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiuj i instaluj zależności Pythona
# (kopiujemy tylko requirements.txt najpierw — Docker cache: warstwa nie przebuduje się jeśli requirements się nie zmienił)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiuj kod (przy dev nadpisany przez volume mount, przy prod potrzebny)
COPY . .
