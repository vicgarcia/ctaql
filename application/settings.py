import os
from configurations import Configuration as configuration


class base(configuration):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SECRET_KEY = os.environ.get('SECRET_KEY')

    DEBUG = False

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'rest_framework',
        'corsheaders',
        #
        'core',
        'users',
        'bustracker',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
    ]

    ROOT_URLCONF = 'urls'

    WSGI_APPLICATION = 'wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'PORT': os.environ.get('POSTGRES_PORT', default='5432'),
        }
    }

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

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
    ]

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 12,
            }
        },
    ]

    AUTH_USER_MODEL = 'users.User'

    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
        'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
        'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    }

    CTA_BUSTRACKER_API_KEY = os.environ.get('CTA_BUSTRACKER_API_KEY')


class production(base):
    pass


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

    # when working locally, emails are not sent and outputted to the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

