import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "versatileimagefield",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "tinymce",
    "apps.users",
    "apps.product",
    "apps.siteconfig",
    "apps.blog",
    "apps.cart",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# STATIC_ROOT = BASE_DIR / 'static'

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    #     'DATE_FORMAT': '%Y-%m-%d',
    #     'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    #     # 'SEARCH_PARAM': 'q',
    "DEFAULT_PAGINATION_CLASS": "libs.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    #     'DEFAULT_PERMISSION_CLASSES': (
    #         # 'rest_framework.permissions.IsAuthenticated',
    #         'rest_framework.permissions.AllowAny',
    #     ),
    #     # 'EXCEPTION_HANDLER': 'libs.drf.exceptions.exception_handler',
    #     'DEFAULT_AUTHENTICATION_CLASSES': [
    #         'rest_framework.authentication.TokenAuthentication'
    #     ],
    #     # 'DEFAULT_THROTTLE_RATES': {
    #     #     'loginAttempts': '12/min',
    #     #     'user': '100/min',
    #     #     'burst': '5/min',
    #     #     'sustained': '50/day'
    #     # }
}

# AUTH_USER_MODEL = 'users.User'

VERSATILEIMAGEFIELD_SETTINGS = {
    "create_images_on_demand": False,
}

AUTH_USER_MODEL = "users.User"
