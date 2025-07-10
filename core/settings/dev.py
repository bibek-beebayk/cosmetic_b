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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./debug.log",
        },
        # "mail_admins": {
        #     "level": "ERROR",
        #     "class": "django.utils.log.AdminEmailHandler",
        #     "include_html": True,
        # },
    },
    "loggers": {
        "": {  # empty string
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# SMTP email configuration
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "beebayk63478@gmail.com"
# EMAIL_HOST_PASSWORD = "yrou cdja nqfc ijhe"
# EMAIL_USE_TLS = True
# FROM_EMAIL = "beebayk63478@gmail.com"

GOOGLE_OAUTH_CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"