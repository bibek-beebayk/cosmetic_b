import os

from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, REST_FRAMEWORK

SECRET_KEY = "django-insecure-e97*el)u=a(#6!r%)6pqxys(myd(ypmr14gd#g+5^ib(urrb!r"

ALLOWED_HOSTS = ["cosmeticb-production.up.railway.app"]

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("PGDATABASE", "cosmetic"),
        "USER": os.environ.get("PGUSER", "postgres"),
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
        "HOST": os.environ.get("PGHOST", ""),
        "PORT": os.environ.get("PGPORT", ""),
        "ATOMIC_REQUESTS": True,
    }
}

CORS_ALLOWED_ORIGINS = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://cosmeticb-production.up.railway.app",
    "https://beautycorner01.netlify.app",
)

CSRF_TRUSTED_ORIGINS = [
    "https://cosmeticb-production.up.railway.app",
    "https://beautycorner01.netlify.app",
]

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)

# INSTALLED_APPS += ['django_extensions', 'debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',
# ]
# INTERNAL_IPS = ['127.0.0.1']

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = "1f8bcff6b47d61799db7beaae02a3fa4"
AWS_SECRET_ACCESS_KEY = (
    "78e32042ccce9896aa5b5767338949146eda472fd532328302be87d2b0ed5260"
)
AWS_STORAGE_BUCKET_NAME = "blackvilla"
AWS_S3_ENDPOINT_URL = (
    "https://b46a64eb384beb50a5fc80946bc0abc7.r2.cloudflarestorage.com/blackvilla"
)
AWS_S3_SIGNATURE_VERSION = "s3v4"

# SMTP email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "beebayk63478@gmail.com"
EMAIL_HOST_PASSWORD = "yrou cdja nqfc ijhe"
EMAIL_USE_TLS = True
FROM_EMAIL = "beebayk63478@gmail.com"

import sentry_sdk

sentry_sdk.init(
    dsn="https://669d879177fa4d23536a8956680897f8@o4506019412180992.ingest.sentry.io/4506019413688320",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
