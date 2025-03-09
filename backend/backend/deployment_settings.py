"""
Django settings for backend project.
"""

import os
import io
from pathlib import Path
from datetime import timedelta

import environ

# ==============================================================================
#                                    BASE
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
#                                   ENV VARS
# ==============================================================================

env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))

# Setting SECRET_KEY from environment variable (important for security)
SECRET_KEY = env("SECRET_KEY")


# ==============================================================================
#                                   CORE Django
# ==============================================================================

DEBUG = True  # TODO: Set to False in production!
ALLOWED_HOSTS = ["*"]  # TODO: Specify your hostnames in production!


# ==============================================================================
#                                  APPLICATIONS
# ==============================================================================

INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Local apps
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware", # allauth middleware
]

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"


# ==============================================================================
#                                   TEMPLATES
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


# ==============================================================================
#                                   DATABASE
# ==============================================================================

DATABASES = {"default": env.db()}

# Use Cloud SQL Auth Proxy if enabled (for local development with Cloud SQL)
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


# ==============================================================================
#                                   STATIC & MEDIA FILES (STORAGES)
# ==============================================================================

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # For collecting static files for deployment
STATICFILES_DIRS = [] # You can add extra static directories here if needed

# Google Cloud Storage settings (using django-storages)
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead" # Set default ACL for uploaded files (consider security implications)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage", # For default file storage (e.g., uploaded media)
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage", # For static files
    },
}


# ==============================================================================
#                                   AUTHENTICATION
# ==============================================================================

AUTH_USER_MODEL = "api.Client" # Custom user model
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend", # Default Django auth backend
    "allauth.account.auth_backends.AuthenticationBackend", # allauth authentication backend
]


# ==============================================================================
#                                   ALLAUTH CONFIGURATION
# ==============================================================================

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "mandatory" # Require email verification
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {"email"} # Only allow login via email

# Social authentication - Google
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
    }
}
SOCIAL_AUTH_GOOGLE_CLIENT_ID = os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
 # Consider using environment variables for these sensitive keys
SOCIAL_AUTH_GOOGLE_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_SECRET') # Consider using environment variables for these sensitive keys


# ==============================================================================
#                                   REST FRAMEWORK
# ==============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication", # Use JWT for authentication
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated", # Require authentication for all API endpoints by default
    ],
}

# JWT settings (simple-jwt)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


# ==============================================================================
#                                   SECURITY
# ==============================================================================

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# CSRF Trusted Origins (for Cloud Run or other deployments where origin might differ)
CSRF_TRUSTED_ORIGINS = ['https://django-cloudrun-9382214662.us-central1.run.app'] # Add your app's domain(s) here


# ==============================================================================
#                                   INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ==============================================================================
#                                   CORS (Cross-Origin Resource Sharing)
# ==============================================================================

CORS_ALLOW_ALL_ORIGINS = True # TODO:  Restrict origins in production for better security!
CORS_ALLOWS_CREDENTIALS = True # Allow sending cookies in CORS requests


# ==============================================================================
#                                   OTHER
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

BASEURL = "http://127.0.0.1:8000" # Development base URL, might not be used directly

# ==============================================================================
#                                   LOGGING
# ==============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG", # Set logging level as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    },
}