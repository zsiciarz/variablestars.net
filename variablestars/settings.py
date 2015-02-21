"""
Django settings for variablestars project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import sys

from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'not-defined-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.variablestars.net']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'autocomplete_light',
    'bootstrap_pagination',
    'compressor',
    'crispy_forms',
    'debug_toolbar',
    'django_extensions',
    'geoposition',
    'south',
    'registration',
    'twitter_bootstrap',
    'raven.contrib.django.raven_compat',

    'observations',
    'observers',
    'stars',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'observers.middleware.ObserverMiddleware',
    'stars.middleware.StarFilterMiddleware',
)

ROOT_URLCONF = 'variablestars.urls'

WSGI_APPLICATION = 'variablestars.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'observers.context_processors.get_current_observer',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = reverse_lazy('auth_login')
LOGOUT_URL = reverse_lazy('auth_logout')
LOGIN_REDIRECT_URL = reverse_lazy('main')

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: u.observer.get_absolute_url(),
}

INTERNAL_IPS = ('127.0.0.1',)

SOUTH_TESTS_MIGRATE = False

CRISPY_TEMPLATE_PACK = 'bootstrap3'

COMPRESS_PARSER = 'compressor.parser.HtmlParser'

RAVEN_CONFIG = {
    'dsn': '',
}

try:
    from local_settings import *  # NOQA
except ImportError:
    pass

if DEBUG:
    import mimetypes
    mimetypes.add_type('text/coffeescript', '.coffee')
else:
    COMPRESS_PRECOMPILERS = (
        ('text/less', '%s {infile} {outfile}' % os.path.join(BASE_DIR, 'node_modules/.bin/lessc')),
        ('text/coffeescript', '%s --compile --stdio' % os.path.join(BASE_DIR, 'node_modules/.bin/coffee')),
    )

if 'test' in sys.argv:
    PASSWORD_HASHERS = {
        'django.contrib.auth.hashers.MD5PasswordHasher',
    }
