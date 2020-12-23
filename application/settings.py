import os
from configurations import Configuration as configuration


class base(configuration):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SECRET_KEY = os.environ.get('SECRET_KEY')

    DEBUG = False

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.staticfiles',
        'rest_framework',
        'graphene_django',
        'bustracker',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
    ]

    ROOT_URLCONF = 'urls'

    WSGI_APPLICATION = 'wsgi.application'

    DATABASES = {}

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

    USE_TZ = True
    TIME_ZONE = 'UTC'

    USE_I18N = False
    USE_L10N = False

    CORS_ORIGIN_ALLOW_ALL = True

    CSRF_USE_SESSIONS = False

    CSRF_COOKIE_HTTPONLY = False

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                ],
            },
        },
    ]

    STATIC_URL = '/static/'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/tmp/django_cache',
        }
    }

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (),
        'DEFAULT_PERMISSION_CLASSES': (),
        'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
        'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
        'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
        'UNAUTHENTICATED_USER': None,
    }

    GRAPHENE = {
        "SCHEMA": "bustracker.schema.schema"
    }

    CTA_BUSTRACKER_API_KEY = os.environ.get('CTA_BUSTRACKER_API_KEY')


class production(base):

    STATIC_ROOT = os.path.join(base.BASE_DIR, 'static')


class development(base):

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
            }
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            }
        }
    }


class local(development):
    pass
