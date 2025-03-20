'''
Boilerplate stuff, import into your own project settings like so:

Conventions:
Using "dproj" as a generic reusable "project" folder instead a unique name every
time (as with the `django-admin startproject` default behavior). "dproj" is also
more grep-able than "project" without false positives. Prefixing all Django-specific
folders with "d" is useful if, e.g., a Flask app is in the same project.
'''
import environ
from django.conf.locale.en import formats as en_formats


# to not clash with similar in a specific project
env2 = environ.Env(DEBUG=(bool, False))

en_formats.DATETIME_FORMAT = 'Y-m-d • H:i:s e'

TSFMT = '%Y-%m-%d %H:%M:%S %z %Z'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEBUG = env2('DEBUG')

SECRET_KEY = env2('DJANGO_SECRET_KEY')

if DEBUG:
    DATABASES = { 'default': env2.db_url('DJANGO_DB_DEV_URL'), }
    ADMIN_HEADER_BG = '#008c00'  # darker green
    LOG_FILE = 'logs/dev.log'         # see LOGGING below
else:
    DATABASES = { 'default': env2.db_url('DATABASE_URL'), }
    ADMIN_HEADER_BG = '#8c0000'  # darker red
    LOG_FILE = 'logs/prod.log'

ROOT_URLCONF = 'dproj.uroot'

WSGI_APPLICATION = 'dproj.wsgi.application'  

# Note that we use Nginx rather than Whitenoise to serve static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_PATH = env2('DJANGO_ADMIN_PATH', default='admin/')

ENV_NAME = env2('DJANGO_ENV_NAME', default='prod')

BASE_APPS = [
    'vto_core',                      # admin templates, custom user model, etc

    # --------------------------------------------------------------------------
    # startproject apps
    # --------------------------------------------------------------------------
    'django.contrib.admin',
    'djinntoux.rename.ContribAuth',   # replaces 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --------------------------------------------------------------------------
    # extra apps
    # --------------------------------------------------------------------------
    'djinntoux.rename.ContribSites',  # replaces 'django.contrib.sites',
    'django.contrib.humanize',        # to render integers in templates
    'djangoql',                       # more powerful than DataTables

    # --------------------------------------------------------------------------
    # optional extra apps
    # --------------------------------------------------------------------------
    # 'compressor'
    # 'django_distill',                        # for static site generation
    # 'django_cachekiller',                    # for static site generation
]


# Always use a minimal custom user app for future flexibility.
# OCD note: the database column has a different label than the actual app name
# (for sorting in psql), which must be used here:
AUTH_USER_MODEL = 'vto_core.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'htmlmin.middleware.HtmlMinifyMiddleware',    # added
    'htmlmin.middleware.MarkRequestMiddleware',   # added
    'djinntoux.middleware.TimezoneMiddleware'  # added
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'djinntoux.templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # extra:
                'djinntoux.context_processors.general'
            ],
        },
    },
]


# Password validation

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

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True

TIME_ZONE = 'UTC'

# ------------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'MYAPP': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}