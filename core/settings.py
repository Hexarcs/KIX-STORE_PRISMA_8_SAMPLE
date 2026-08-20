import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Puxa a chave do .env; se não achar, usa um fallback temporário
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-local-key')

# Converte o valor de DEBUG do .env para Booleano
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# ⚡ OBRIGATÓRIO PARA HTTPS: Permite requisições POST (como o add do carrinho) vindas do seu domínio
CSRF_TRUSTED_ORIGINS = [
    'https://engine-99.libertariamemes.com.br',
    'https://supermercado.hexarcs.com.br',
     'https://supermercado.hexarcs.com',
]


# Application definition

INSTALLED_APPS = [
    'core',  # 🌟 Adicione isso aqui para o Django rastrear seus modelos!
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Módulos obrigatórios para o Allauth funcionar
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 🌟 ADICIONE ESTA LINHA AQUI PARA ATIVAR O GOOGLE:
    'allauth.socialaccount.providers.google',
]

# Configuração do ID do site (obrigatório para o django.contrib.sites)
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # 🌟 ADICIONE ESTA LINHA EXATAMENTE AQUI:
    'allauth.account.middleware.AccountMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 🌟 Modifique ESTA linha abaixo:
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Essencial para o Allauth injetar dados do usuário na tela
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ADICIONE ESTA LINHA AQUI:
                'core.context_processors.btc_context',                
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
########-----------------------------------------------##############
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# 1. Rota de URL para arquivos estáticos
STATIC_URL = '/static/'

# 2. Onde o Django vai buscar os estáticos em modo Desenvolvimento (Resolve o script.js)
STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]

# 3. Onde o Django vai agrupar tudo para produção ao rodar o collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"


# --- Autenticação e resto das suas configurações que já estavam aí ---

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Redirecionamentos pós-login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Customizações do Allauth (Sintaxe Estrita Atualizada)
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*']  # O '*' resolve o erro crítico de e-mail obrigatório
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SESSION_REMEMBER = True

# Envia os e-mails de confirmação para o console do servidor por enquanto
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
########---------------------------------------------------##############


