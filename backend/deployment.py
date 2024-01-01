import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = False
CORS_ALLOW_ALL_ORIGINS = True


MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


CONNECTION_STRING = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']

PARAM = {
    pair.split('=')[0]: pair.split('=')[1] for pair in CONNECTION_STRING.split(' ')
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PARAM['dbname'],
        'USER': PARAM['user'],
        'PASSWORD': PARAM['password'],
        'HOST': PARAM['host'],
        'PORT': PARAM['port'],
    }
}