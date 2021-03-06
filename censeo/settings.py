# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys

from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'auth.User'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'censeo',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'censeo.context_processors.constants',
            ],
        },
    },
]
ROOT_URLCONF = 'censeo.urls'
WSGI_APPLICATION = 'censeo.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_COMPILERS = ('pipeline.compilers.less.LessCompiler',)
PIPELINE_YUGLIFY_BINARY = os.path.join(BASE_DIR, 'node_modules/.bin/yuglify')
PIPELINE_LESS_BINARY = os.path.join(BASE_DIR, 'node_modules/.bin/lessc')
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'censeo/libs/bootstrap/css/bootstrap.css',
            'censeo/less/base.less',
        ),
        'output_filename': 'css/base.min.css',
    },
    'meet': {
        'source_filenames': (
            'censeo/libs/jquery.ui/css/jquery-ui-theme/jquery-ui-1.10.4.custom.css',
        ),
        'output_filename': 'css/meet.min.css',
    },
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'censeo/libs/jquery.maskedinput/jquery.maskedinput.js',
            'censeo/libs/bootstrap/js/bootstrap.js',
            'censeo/libs/underscore/underscore-min.js',
            'censeo/libs/jquery.cookie/jquery.cookie.js',
            'censeo/libs/jquery.csrf/jquery.csrf.js',
            'censeo/libs/spin.js/spin.js',
            'censeo/js/base.js',
        ),
        'output_filename': 'js/base.min.js',
    },
    'meet': {
        'source_filenames': (
            'censeo/libs/jquery.ui/js/jquery-ui-1.10.4.custom.js',
            'censeo/js/meet.js',
        ),
        'output_filename': 'js/meet.min.js',
    }
}

# Test settings
if 'test' in sys.argv:
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = ['--nocapture', '--with-coverage', '--cover-html', '--cover-erase',
                 '--cover-branches', '--cover-package=censeo', '-e=settings.py']

# Registration
LOGIN_REDIRECT_URL = reverse_lazy('meet')
ACCOUNT_ACTIVATION_DAYS = 3

# Ticket Settings
TICKET_REGEX = r'LON-\d{4}'
# The TICKET_MASK_* settings are used to configure the jQuery Masked Input Plugin
# See http://digitalbush.com/projects/masked-input-plugin/#usage for more information
TICKET_MASK_DEFINITIONS = {
    'L': '[Ll]',
    'O': '[Oo]',
    'N': '[Nn]',
}
TICKET_MASK = 'LON-9999'
TICKET_URL = '//jira2.cerner.corp/browse/{ticket_number}'

if 'runserver' in sys.argv:
    EMAIL_PORT = 1025
