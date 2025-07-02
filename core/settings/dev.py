from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = 'django-insecure-e97*el)u=a(#6!r%)6pqxys(myd(ypmr14gd#ge+5^ib(urrb!r'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'tunnel.quiznfacts.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cosmetic',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

CORS_ALLOWED_ORIGINS = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
    "https://fetunnel.quiznfacts.com"
)

INSTALLED_APPS += ['django_extensions', 'debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1']