# -*- coding: utf-8 -*-
import os.path
import dj_database_url

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sergiy Khalymon', 'sergiykhalimon@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite')
}

### For Postgres
# DATABASES['default'] =  dj_database_url.config()
# DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': '',                      # Or path to database file if using sqlite3.
#         # The following settings are not used with sqlite3:
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',                      # Set to empty string for default.
#     }
# }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

SITE_ID = 1

### Interalization ###
USE_I18N = True
USE_L10N = True
USE_TZ = True

### Media ###
MEDIA_ROOT = ''
MEDIA_URL = ''

### Static ###
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'friends_on_map.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'friends_on_map.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'gunicorn',
    'south',
    'social.apps.django_app.default',
    'auth',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

### For Python Social Auth ###
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
)

AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    # 'social.backends.google.GoogleOAuth',
    # 'social.backends.google.GooglePlusAuth',

    'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.vk.VKOAuth2',
    # 'social.backends.email.EmailAuth',
    # 'social.backends.username.UsernameAuth',
    #'social.apps.django_app.utils.BackendWrapper',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/done'
LOGIN_URL = '/login/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
# SOCIAL_AUTH_STORAGE = 'auth.models.DjangoStorage'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    # 'auth.app.pipeline.require_email',
    # 'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    # 'auth.pipeline.get_user_friends',
    'auth.pipeline.get_user_avatar',
    'social.pipeline.user.user_details',


)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect'
)

SOCIAL_AUTH_FACEBOOK_KEY = '223307271163808'
SOCIAL_AUTH_FACEBOOK_SECRET = '94cda17962cf0d13188880c3be3d82a0'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
#SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}
#SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [('friends', '')]
SOCIAL_AUTH_VK_OAUTH2_KEY = '3972093'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'dlrYrcLQrA1dUdF8nAlE'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'friends']
# SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = [('friends','friends.get')]


GMAP_API_KEY = 'AIzaSyDpn1J5RZp3-Ko0wjRRlQNb0Q_DQGi951M'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '91es7q)2)4l%fukw30pji=gj^ah#871r11+8v-j+0fev(5^z$^'


try:
    from .local import *
except ImportError:
    pass