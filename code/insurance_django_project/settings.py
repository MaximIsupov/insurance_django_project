"""
Django settings for insurance_django_project project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dc9)tfmqs#*ps(c00!m@m%t797=$whe*0rc(b-pic%-u^akc7s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'insurance_app.apps.InsuranceAppConfig',
    'django_elasticsearch_dsl',
    'rest_framework',
]

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv("ELASTICSEARCH_DSL_HOSTS", 'es:9200')
    },
}

RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER', 'admin')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS', 'admin')
CELERY_BROKER_URL = f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq:5672'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'insurance_django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'insurance_django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("POSTGRES_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("POSTGRES_DB", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    },
    'mongo': {
        'NAME': os.environ.get("MONGO_DB_NAME", "mongo_db"),
        'ENGINE': 'djongo',
        'USER': os.environ.get("MONGO_DB_USERNAME", "root"),
        'PASSWORD': os.environ.get("MONGO_DB_PASSWORD", "root"),
        "PORT": os.environ.get("MONGO_DB_PORT", "27017"),
        "HOST": os.environ.get("MONGO_DB_HOST", "mongo"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/code/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@sandbox2db3da92e61945a69c986c41973a704d.mailgun.org' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = 'ba90c1f11af9e7eab25dfaea585de9a4-1b237f8b-31cae994'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

