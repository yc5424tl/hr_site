
import os
import uuid
from pathlib import Path
from hr_access.models import User as CustomUser
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEPLOYMENT = os.getenv("DEPLOYMENT")
ALLOWED_HOSTS = ['127.0.0.1:8000', 'localhost:8000', 'hellareptilian.com']
SECURE_SSL_REDIRECT = True
AUTH_USER_MODEL = CustomUser

# learndjango.com/tutorials/django-best-practices-security
if DEPLOYMENT == "PROD":
    SECURE_HSTS_SECONDS = 2592000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

if DEPLOYMENT == "DEV":
    import dotenv

    DJANGO_READ_DOT_ENV_FILE = True

    dotenv_file = os.path.join(BASE_DIR, "../.env.dev")

    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)


DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", str(uuid.uuid4()))
DEBUG = int(os.environ.get("DEBUG", default=0))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djstripe',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'hr_django.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'hr_django.wsgi.application'


DATABASES = {
    'default': {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES["default"].update(db_from_env)


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# STRIPE KEYS
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_LIVE_MODE = os.environ.get("STRIPE_LIVE_MODE") == "TRUE"
DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET", default=str(uuid.uuid4()) )
DJSTRIPE_USE_NATIVE_JSONFIELD = os.environ.get("DJSTRIPE_USE_NATIVE_JSONFIELD") == "TRUE"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"


if DEBUG == "TRUE":
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    BETTER_EXCEPTIONS = 1
    INTERNAL_IPS = type(str("c"), (), {"__contains__": lambda *a: True})()
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
    ]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CONFIG": show_toolbar,
        "SHOW_COLLAPSED": False,
        "SQL_WARNING_THRESHOLD": 500,
    }
