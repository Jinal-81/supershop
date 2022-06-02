"""
Django settings for supershop project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import logging
import os
import datetime
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mc@%#g7&(5g3xw0(kk!6h2^h2m)(w4z#&*f@27!o!pp@2aucv9'

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
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    # 'userlogin',
    # 'cart',
    # 'product',
    'django_filters',
    'django_rest_passwordreset',
    'django_extensions',
]

MY_APPS = [
    'userlogin',
    'cart',
    'product'
]

INSTALLED_APPS += MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userlogin.custom_middleware.DemoMiddleware',
    # 'userlogin.AuthMiddleware.authenticate',
]

ROOT_URLCONF = 'supershop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('userlogin', 'templates')],
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

WSGI_APPLICATION = 'supershop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SuperShop',
        'USER': 'myuser',
        'PASSWORD': 'mypass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")
# print(STATIC_ROOT)
# BASE URL TO SERVER MEDIA FILES
MEDIA_URL = '/media/'
LOGIN_URL = '/login/'

# path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

TOKEN_EXPIRED_AFTER_SECONDS = 5
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# GDAL_LIBRARY_PATH = '/opt/homebrew/opt/gdal/lib/libgdal.dylib'
# GEOS_LIBRARY_PATH = '/opt/homebrew/opt/geos/lib/libgeos_c.dylib'
AUTH_USER_MODEL = 'userlogin.MyUser'
DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'userlogin.authentication.SafeJWTAuthentication',
    # ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter'],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ('v1', 'v2', 'v5', ),
    'VERSION_PARAM': 'version',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Put the number of items you desire
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=20)  # set the access token expired time.
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # custom formate for the logger message
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'debug.log',
            'when': 'S',
            'interval': 1,
            'backupCount': 5,  # last 5 files show
            'formatter': 'verbose',
        },
        'cart': {  # handler for the cart app info level
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'CART_INFO.log',
            'when': 'm',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'verbose',

        },
        'cart_debug': {  # handler for the cart app debug level
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': 'CART_DEBUG.log',
            'mode': 'a',
            'encoding': None,
            'delay': False,
            'formatter': 'verbose',
        },
        'cart_warning': {  # handler for the cart app warning level
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'CART_WARNING.log',
            'formatter': 'verbose',
        },
        'product_info': {  # handler for the product app info level
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'PRODUCT_INFO.log',
            'maxBytes': 42000,
            'backupCount': 5,  # this is required if we want to know the changes.
            'formatter': 'verbose',
        },
        'product_debug': {  # handler for the product app debug level
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'PRODUCT_DEBUG.log',
            'formatter': 'verbose',
        },
        'product_warning': {  # handler for the product app warning level
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'PRODUCT_WARNING.log',
            'formatter': 'verbose',
        },
        'userlogin_info': {  # handler for the userlogin app info level
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'USERLOGIN_INFO.log',
            'formatter': 'verbose',
        },
        'userlogin_debug': {  # handler for the userlogin app debug level
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'USERLOGIN_DEBUG.log',
            'formatter': 'verbose',
        },
        'userlogin_warning': {  # handler for the userlogin app warning level
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'USERLOGIN_WARNING.log',
            'formatter': 'verbose',
        },
        'console': {  # handler for the console.
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cart': {  # logger for the cart app info level
            'handlers': ['console', 'cart'],
            'level': 'INFO',
        },
        'cart_debug': {  # logger for the cart app debug level
            'handlers': ['console', 'cart_debug'],
            'level': 'DEBUG',
        },
        'cart_warning': {  # logger for the cart app warning level
            'handlers': ['console', 'cart_warning'],
            'level': 'WARNING',
        },
        'product_info': {  # logger for the product app info level
            'handlers': ['console', 'product_info'],
            'level': 'INFO',
        },
        'product_debug': {  # logger for the product app debug level
            'handlers': ['console', 'product_debug'],
            'level': 'DEBUG',
        },
        'product_warning': {  # logger for the product app warning level
            'handlers': ['console', 'product_warning'],
            'level': 'WARNING',
        },
        'userlogin_info': {  # logger for the userlogin app info level
            'handlers': ['console', 'userlogin_info'],
            'level': 'INFO',
        },
        'userlogin_debug': {  # logger for the userlogin app debug level
            'handlers': ['console', 'userlogin_debug'],
            'level': 'DEBUG',
        },
        'userlogin_warning': {  # logger for the userlogin app warning level
            'handlers': ['console', 'userlogin_warning'],
            'level': 'WARNING',
        }
    },
}