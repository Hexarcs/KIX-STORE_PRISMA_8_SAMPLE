# Tutorial: Automatizando a Criação de uma Nova Instância (Loja) via Script Shell

Este guia prático ensina como criar e utilizar um script automatizado para subir uma nova instância isolada do sistema na porta `8007`.

A instância será criada na pasta `~/Hexarcs_loja`, terá volumes persistentes para `data` e `media`, um arquivo `.env` com variáveis de configuração e um `docker-compose.yml` configurado para criar automaticamente o superusuário do Django.

## Passo 1: Criar o arquivo do script

Abra o terminal e crie o arquivo de automação usando o editor `nano`:

```bash
nano criar_loja_8007.sh
```

## Passo 2: Inserir o código do script

Cole o conteúdo abaixo dentro do editor.

> **Nota:** As credenciais e chaves sensíveis foram substituídas por placeholders educativos, como `suaapikeycoinsaqui`, `suaapikeylnbitsaqui` e `SuaSenhaSeguraAqui`.

```bash
#!/bin/bash

# Define o diretório da nova loja na home
LOJA_DIR="$HOME/Hexarcs_loja"

echo "Criando a estrutura da nova loja em: $LOJA_DIR..."
mkdir -p "$LOJA_DIR/data"
mkdir -p "$LOJA_DIR/media"

# Cria o arquivo .env com valores de aprendizado/exemplo
echo "Escrevendo o arquivo .env..."
cat << 'EOF' > "$LOJA_DIR/.env"
COINAPI_KEY=suaapikeycoinsaqui
LNBITS_API_KEY=suaapikeylnbitsaqui
LNBITS_URL=https://seuendpointlnbitsaqui/api/v1/payments
SECRET_KEY=django-insecure-suachavesecretadeaprendizadoaqui
DEBUG=True
ALLOWED_HOSTS=*
EOF

# Cria o arquivo docker-compose.yml
echo "Criando o docker-compose.yml..."
cat << 'EOF' > "$LOJA_DIR/docker-compose.yml"
services:
  web:
    image: zeloko/supermercado-kix:latest
    container_name: hexarcs_loja_8007

    ports:
      - "8007:8000"

    volumes:
      - ./data:/app/data
      - ./media:/app/media

    env_file:
      - .env

    environment:
      - DEBUG=1
      - DJANGO_SUPERUSER_USERNAME=admin
      - DJANGO_SUPERUSER_EMAIL=admin@exemplo.com
      - DJANGO_SUPERUSER_PASSWORD=SuaSenhaSeguraAqui

    command: >
      sh -c "python manage.py migrate &&
      python manage.py createsuperuser --noinput || true &&
      python manage.py runserver 0.0.0.0:8000"

    restart: unless-stopped
EOF

# Ajusta as permissões de dono da pasta
sudo chown -R "$USER:$USER" "$LOJA_DIR"

echo "Tudo pronto! Subindo o container da nova loja na porta 8007..."
cd "$LOJA_DIR"
docker compose up -d

echo "Loja criada e rodando com sucesso!"
```

> **Dica do Nano:** Pressione `Ctrl + O` e depois `Enter` para salvar. Em seguida, pressione `Ctrl + X` para sair do editor.

## Passo 3: Conceder permissão de execução

Com o script salvo, torne-o executável:

```bash
chmod +x criar_loja_8007.sh
```

## Passo 4: Executar o script

Execute o script diretamente no terminal:

```bash
./criar_loja_8007.sh
```

O script irá automaticamente:

1. Criar a pasta `~/Hexarcs_loja`.
2. Criar os diretórios persistentes `data` e `media`.
3. Criar o arquivo `.env`.
4. Criar o `docker-compose.yml`.
5. Configurar a aplicação na porta `8007`.
6. Executar as migrações do Django.
7. Criar o superusuário `admin`.
8. Iniciar o container Docker em segundo plano.

Ao final, a loja estará disponível na porta:

```text
http://SEU_SERVIDOR:8007
```

## Estrutura criada

A estrutura final será semelhante a:

```text
~/Hexarcs_loja/
├── .env
├── docker-compose.yml
├── data/
└── media/
```

O container será executado com o nome:

```text
hexarcs_loja_8007
```

## Verificar o container

Para verificar se a loja está rodando:

```bash
docker ps
```

Para visualizar os logs:

```bash
cd ~/Hexarcs_loja
docker compose logs -f
```

Para parar a loja:

```bash
cd ~/Hexarcs_loja
docker compose down
```
