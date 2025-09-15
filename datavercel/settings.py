import os
from pathlib import Path
import dj_database_url
from decouple import config, Csv # Importe 'config' e 'Csv'
from urllib.parse import quote_plus # Importe para codificar a senha

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use python-decouple para ler as variáveis de ambiente
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)


# --- INÍCIO DA CORREÇÃO 1: ALLOWED_HOSTS ---
# Esta seção foi alterada para ler a VERCEL_URL automaticamente

# Obter a VERCEL_URL injetada pelo Vercel, se existir
VERCEL_DEPLOY_URL = os.environ.get('VERCEL_URL')

# Começa com hosts padrões para desenvolvimento local
hosts = ['127.0.0.1', 'localhost']

if VERCEL_DEPLOY_URL:
    hosts.append(VERCEL_DEPLOY_URL)

# Lê a variável de ambiente ALLOWED_HOSTS (que você pode definir no Vercel)
# Se não estiver definida, usa a lista 'hosts' que acabamos de criar.
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default=','.join(hosts),
    cast=Csv()
)
# --- FIM DA CORREÇÃO 1 ---


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Adicionado
    'django.contrib.staticfiles',
    'core', # Adicione seu app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Adicione esta linha
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datavercel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Adicione esta linha para templates globais
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'datavercel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Monta a URL do banco de dados programaticamente para lidar com senhas
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = quote_plus(config('DB_PASSWORD')) # Codifica a senha
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# --- INÍCIO DA CORREÇÃO 2: DATABASE SSL ---
# Adicionado 'ssl_require=True' para conectar ao Supabase

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL, 
        conn_max_age=600,
        ssl_require=True  # <-- ADICIONADO PARA CONEXÃO COM SUPABASE
    )
}
# --- FIM DA CORREÇÃO 2 ---


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Bahia'
USE_I1N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # Se você tiver uma pasta static global
STATIC_ROOT = BASE_DIR / 'staticfiles' # O WhiteNoise usará esta pasta
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'