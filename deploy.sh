#!/bin/bash

# Ativa o ambiente virtual
source venv/bin/activate

# Detecta a mudança no models.py e cria o arquivo de migração
python manage.py makemigrations

# Aplica a alteração de fato no seu banco de dados
python manage.py migrate

# Mata processos antigos do Django
sudo kill -9 $(pgrep -f "manage.py") 2>/dev/null

# Inicia o servidor em segundo plano
nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &

echo "Servidor reiniciado com sucesso!"
