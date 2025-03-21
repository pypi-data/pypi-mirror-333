# -*- coding: utf-8 -*-
"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

"""

import logging
import logging.config
import socket
import sys
from os import environ
from pathlib import Path

import byuhbll_configuro as configuro

from .logging import config as default_logging_config

# CONFIGURATION SETUP
# ------------------------------------------------------------------------------

# Load the configs
BASE_DIR = Path.cwd().absolute()
config = configuro.load(config_filename='application.yml')
settings = sys.modules[__name__]

dict_configs = config.dict_copy()

# django settings go in the root
django_settings = dict_configs.get('django', {})
for setting, value in django_settings.items():
    setattr(settings, setting.upper(), value)

# all other settings go in section specific settings dicts
excluded_sections = ['django', 'extends', 'meta']
for section in [k for k in dict_configs if k not in excluded_sections]:
    setattr(settings, section.upper(), {})
    section_settings = getattr(settings, section.upper())
    for setting, value in dict_configs.get(section, {}).items():
        section_settings[setting.upper()] = value

DEBUG = bool(settings.DEBUG)

# DRY SETTINGS AND DEFAULTS
# ------------------------------------------------------------------------------
dry_settings = settings.DRY
# required
project_identifier = dry_settings['PROJECT_IDENTIFIER']
project_slug = dry_settings['PROJECT_SLUG']

# optional
dry_settings['SECURE_COOKIES'] = bool(dry_settings.get('SECURE_COOKIES', False))

dry_settings['PORT'] = dry_settings.get('PORT', 8080)
dry_settings['ADMIN_URL_PATH'] = dry_settings.get('ADMIN_URL_PATH', 'admin/').lstrip(
    '/'
)
dry_settings['LOGIN_URL_PATH'] = dry_settings.get('LOGIN_URL_PATH', 'login/').lstrip(
    '/'
)
dry_settings['LOGOUT_URL_PATH'] = dry_settings.get('LOGOUT_URL_PATH', 'logout/').lstrip(
    '/'
)

dry_settings['LOGGING'] = dry_settings.get(
    'LOGGING',
    {
        'root_level': 'DEBUG' if DEBUG else 'INFO',
        'root_handlers': ['console'],
        'console_formatter': 'color' if DEBUG else 'default',
        'ignored_loggers': [],
        'django_loggers': {},
        'override': {},
    },
)

# SETTING UP DJANGO SETTING DEFAULTS
# ------------------------------------------------------------------------------

INSTALLED_APPS = django_settings.get(
    'installed_apps',
    [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django_extensions',
        'django_filters',
        'hijack',
        'hijack.contrib.admin',
        'users',
        'rest_framework',
        project_identifier,
    ],
)

MIDDLEWARE = django_settings.get(
    'middleware',
    [
        'byuhbll_django_dry.middleware.PingViewMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'hijack.middleware.HijackUserMiddleware',
    ],
)

SERVER_EMAIL = django_settings.get('server_email', 'noreply@lib.byu.edu')
DEFAULT_FROM_EMAIL = django_settings.get(
    'default_from_email', f'{project_slug}@lib.byu.edu'
)
EMAIL_SUBJECT_PREFIX = django_settings.get('email_subject_prefix', f'[{project_slug}] ')

TIME_ZONE = django_settings.get('time_zone', 'America/Denver')
LANGUAGE_CODE = django_settings.get('language_code', 'en-us')

USE_I18N = bool(django_settings.get('use_i18n', False))
USE_L10N = bool(django_settings.get('use_l10n', True))
USE_TZ = bool(django_settings.get('use_tz', True))

TEMPLATES = django_settings.get(
    'templates',
    [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],  # for template dirs not in app_name/templates
            'APP_DIRS': True,  # autodiscovers templates in app_name/templates
            'OPTIONS': {
                'debug': DEBUG,
                'string_if_invalid': '!!missing!!' if DEBUG else '',
                'context_processors': [
                    # defaults
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }
    ],
)

force_script_name_path = django_settings.get('force_script_name', '').rstrip('/')

FORCE_SCRIPT_NAME = force_script_name_path

STATICFILES_STORAGE = django_settings.get(
    'staticfiles_storage',
    'whitenoise.storage.CompressedManifestStaticFilesStorage',
)
STATIC_ROOT = django_settings.get('static_root', BASE_DIR / 'static')
STATIC_URL = django_settings.get('static_url', f'{force_script_name_path}/static/')
WHITENOISE_STATIC_PREFIX = '/static/'
MEDIA_ROOT = django_settings.get('media_root', BASE_DIR / 'media')
MEDIA_URL = django_settings.get('media_url', f'{force_script_name_path}/media/')

USE_X_FORWARDED_HOST = bool(django_settings.get('use_x_forwarded_host', True))
SECURE_PROXY_SSL_HEADER = django_settings.get(
    'secure_proxy_ssl_header', ('HTTP_X_FORWARDED_PROTO', 'https')
)
ALLOWED_HOSTS = django_settings.get('allowed_hosts', ['localhost', '127.0.0.1'])
HTTP_X_FORWARDED_HOST = django_settings.get('http_x_forwarded_host', 'localhost')

SESSION_COOKIE_SECURE = django_settings.get(
    'session_cookie_secure', dry_settings['SECURE_COOKIES']
)
CSRF_COOKIE_SECURE = django_settings.get(
    'csrf_cookie_secure', dry_settings['SECURE_COOKIES']
)

SESSION_COOKIE_AGE = int(
    django_settings.get('session_cookie_age', 7200)
)  # default 2 hours
SESSION_SAVE_EVERY_REQUEST = bool(
    django_settings.get('session_save_every_request', True)
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = bool(
    django_settings.get('session_expire_at_browser_close', True)
)
SESSION_COOKIE_HTTPONLY = bool(django_settings.get('session_cookie_httponly', True))
SECURE_BROWSER_XSS_FILTER = bool(django_settings.get('secure_browser_xss_filter', True))
SECURE_CONTENT_TYPE_NOSNIFF = bool(
    django_settings.get('secure_content_type_nosniff', True)
)

# https://docs.djangoproject.com/en/3.2/ref/middleware/#ssl-redirect
SECURE_SSL_REDIRECT = bool(django_settings.get('secure_ssl_redirect', False))
X_FRAME_OPTIONS = django_settings.get('x_frame_options', 'DENY')

ROOT_URLCONF = django_settings.get('root_urlconf', 'project.urls')
WSGI_APPLICATION = django_settings.get(
    'wsgi_application', 'byuhbll_django_dry.wsgi.application'
)

LOGIN_URL = django_settings.get('login_url', f'{force_script_name_path}/login/')
LOGOUT_URL = django_settings.get('logout_url', f'{force_script_name_path}/logout/')

admin_path = dry_settings['ADMIN_URL_PATH']
LOGIN_REDIRECT_URL = django_settings.get(
    'login_redirect_url', f'{force_script_name_path}/{admin_path}'
)

LOGOUT_REDIRECT_URL = django_settings.get(
    'logout_redirect_url', f'{force_script_name_path}/{admin_path}'
)

AUTH_USER_MODEL = django_settings.get('auth_user_model', 'users.User')

CACHES = django_settings.get(
    'caches',
    {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
)

DATABASES = django_settings.get(
    'databases',
    {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
LOGGING_CONFIG = django_settings.get('logging_config', None)

if not LOGGING_CONFIG:
    # Change default_logging_config here before setting it as the logging
    # configuration below.
    default_log_level = default_logging_config['loggers']['']['level']
    default_log_handlers = default_logging_config['loggers']['']['handlers']
    default_console_formatter = default_logging_config['handlers']['console'][
        'formatter'
    ]
    if DEBUG:
        default_log_level = 'DEBUG'
        default_log_handlers = ['console']
        default_console_formatter = 'color'

    dry_logging = dry_settings['LOGGING']
    root_level = dry_logging.get('root_level', default_log_level)
    root_handlers = dry_logging.get('root_handlers', default_log_handlers)
    console_formatter = dry_logging.get('console_formatter', default_console_formatter)

    logging_config = default_logging_config.copy()
    logging_config['loggers']['']['level'] = root_level
    logging_config['loggers']['']['handlers'] = root_handlers
    logging_config['handlers']['console']['formatter'] = console_formatter

    # silence logs of noisy packages that aren't helpful
    logging_config['loggers'].update(
        {
            m: {'level': 'NOTSET', 'propagate': False}
            for m in dry_logging.get('ignored_loggers', [])
        }
    )

    # changing log levels for django modules
    logging_config['loggers'].update(
        {
            module: {'level': level}
            for module, level in dry_logging.get('django_loggers', {}).items()
        }
    )

    # override logging configuration
    override = dry_logging.get('override', {})

    if override:
        logging_config = configuro.merge(logging_config, override)

    # Set logging configuration
    logging.config.dictConfig(logging_config)

# THIRD-PARTY APP SETTINGS DEFAULTS
# ------------------------------------------------------------------------------
# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = getattr(
    settings,
    'REST_FRAMEWORK',
    {
        'DEFAULT_PERMISSION_CLASSES': [
            # for public apis authorization
            'byuhbll_django_dry.permissions.HasAPIGroupPermission',
            # for ajax apis authorizations
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            # for public apis auth
            'rest_framework.authentication.BasicAuthentication',
            # for ajax apis auth
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
    },
)

# DEBUG MODE DEFAULTS
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    INSTALLED_APPS.insert(0, 'livereload')
    INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    MIDDLEWARE.append('livereload.middleware.LiveReloadScript')

    _, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1']

    # set default dev server port
    RUNSERVERPLUS_SERVER_ADDRESS_PORT = str(dry_settings['PORT'])

    # Set django-livereload-server to run on the same port + 20000
    default_livereload_port = dry_settings['PORT'] + 20000
    LIVERELOAD_PORT = environ.get('LIVERELOAD_PORT', default_livereload_port)
    LIVERELOAD_HOST = '0.0.0.0'

    # shut off some security settings for development
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'

AUTHENTICATION_BACKENDS = getattr(
    settings,
    'AUTHENTICATION_BACKENDS',
    ['django.contrib.auth.backends.ModelBackend'],
)

# OIDC
oidc = getattr(settings, 'OIDC', {})
settings.OIDC = oidc
oidc['ENABLED'] = bool(oidc.get('ENABLED', False))

if oidc['ENABLED']:
    for setting, value in oidc.items():
        if setting in {'ENABLED'}:
            continue
        setattr(settings, f'OIDC_{setting}', value)

    OIDC_RP_SIGN_ALGO = getattr(settings, 'OIDC_RP_SIGN_ALGO', 'RS256')
    OIDC_OP_JWKS_ENDPOINT = getattr(
        settings,
        'OIDC_OP_JWKS_ENDPOINT',
        'https://keycloak.lib.byu.edu/realms/ces/protocol/openid-connect/certs',
    )
    OIDC_OP_AUTHORIZATION_ENDPOINT = getattr(
        settings,
        'OIDC_OP_AUTHORIZATION_ENDPOINT',
        'https://keycloak.lib.byu.edu/realms/ces/protocol/openid-connect/auth',
    )
    OIDC_OP_TOKEN_ENDPOINT = getattr(
        settings,
        'OIDC_OP_TOKEN_ENDPOINT',
        'https://keycloak.lib.byu.edu/realms/ces/protocol/openid-connect/token',
    )
    OIDC_OP_USER_ENDPOINT = getattr(
        settings,
        'OIDC_OP_USER_ENDPOINT',
        'https://keycloak.lib.byu.edu/realms/ces/protocol/openid-connect/userinfo',
    )
    OIDC_USERNAME_ALGO = getattr(settings, 'OIDC_USERNAME_ALGO', lambda x: x)
    OIDC_STORE_ACCESS_TOKEN = bool(getattr(settings, 'OIDC_STORE_ACCESS_TOKEN', False))
    ALLOW_LOGOUT_GET_METHOD = True

    INSTALLED_APPS.insert(
        INSTALLED_APPS.index('django.contrib.auth') + 1, 'mozilla_django_oidc'
    )

    AUTHENTICATION_BACKENDS.append('byuhbll_django_dry.auth.DryOIDCAuthBackend')
