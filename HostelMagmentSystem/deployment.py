from .settings import *
import os
from . settings import BASE_DIR
import dj_database_url

DEBUG= False
ALLOWED_HOSTS= [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
CSRF_TRUSTED_ORIGINS =['https://'+os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
SECRET_KEY = os.environ.get('SECRET_KEY')
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware"
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]


CORS_ALLOWED_ORIGINS = [
    # "http://localhost:3000",  
    # "http://127.0.0.1:3000",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


CONNECTION = os.environ['AZURE_POSTGRESQL_CONNECTION_STRING']
CONNECTION_STR = {pair.split('=')[0]: pair.split('=')[1] for pair in CONNECTION.split(' ')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': CONNECTION_STR['dbname'], 
        'HOST': CONNECTION_STR['host'], 
        'USER': CONNECTION_STR['user'],
        'PASSWORD': CONNECTION_STR['password'],
        
    }
}

STATIC_ROOT =  BASE_DIR / 'staticfiles'


