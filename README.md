# 🛒 Supermercado KIX

Um portal de e-commerce e caixa de atendimento integrado ao **Ecossistema KIX**, desenvolvido em Python e Django. O sistema permite liquidação nativa de pagamentos em **Bitcoin / Satoshis via Lightning Network** (com desconto) ou integração com pagamentos tradicionais.

> ⚠️ **Status do Projeto:** Atualmente rodando em arquitetura **Django Baremetal**. A gestão de produtos, categorias, preços e mídias é realizada diretamente pelo painel administrativo nativo do Django (`/admin`).

---

## 🚀 Guia de Inicialização Rápida (Para Novatos)

Se você acabou de clonar o repositório, siga o passo a passo abaixo para "compilar" a aplicação no seu ambiente local (instalar dependências, preparar o banco de dados e subir o servidor).

### 1. Clonar o Repositório
```bash
git clone https://github.com/Hexarcs/supermercado_kix.git
cd supermercado_kix
```

### 2. Criar e Ativar o Ambiente Virtual (`venv`)
```bash
# Cria o ambiente virtual isolado
python3 -m venv venv

# Ativa o venv no Linux/macOS
source venv/bin/activate

# (No Windows PowerShell use: .\venv\Scripts\Activate.ps1)
```

### 3. Instalar as Dependências do Python
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente (`.env`)
Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo base:

```env
SECRET_KEY=sua-chave-secreta-django-dev
DEBUG=True
ALLOWED_HOSTS=*
COINAPI_KEY=sua_chave_coinapi_aqui
LNBITS_API_KEY=sua_chave_lnbits_aqui
LNBITS_URL=https://sua-instancia-lnbits/api/v1/payments
```

### 5. Preparar o Banco de Dados (Migrations)
Execute as migrações para criar as tabelas necessárias no SQLite:

```bash
python manage.py migrate
```

### 6. Criar o Usuário Administrador
Crie o acesso para gerenciar a loja pelo painel do Django:

```bash
python manage.py createsuperuser
```

### 7. Subir a Aplicação
Inicie o servidor de desenvolvimento na porta desejada (ex: `8000` ou `9889`):

```bash
python manage.py runserver 0.0.0.0:8000
```

Acesse no seu navegador: **`http://localhost:8000`**

---

## 🛠️ Personalização via Django Admin

Como a estrutura atual roda em formato *baremetal*, toda a customização da loja é feita pelo painel `/admin`:

1. Acesse `http://localhost:8000/admin` e faça login com a conta criada no `createsuperuser`.
2. **Produtos & Categorias:** Cadastre os itens que aparecerão na vitrine principal.
3. **Login Social (Opcional):** Se desejar ativar o login via Google em ambiente local, navegue até **Social Accounts > Social Applications** e associe a aplicação Google ao `Site ID 1`. Caso não cadastre, o sistema utilizará a tela de login tradicional automaticamente.

---

