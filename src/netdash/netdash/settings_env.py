"""
Django settings for NetDash project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import dj_database_url


def csv_to_list(csv, delim=','):
    try:
        return [x.strip() for x in csv.split(delim) if x.strip()]
    except Exception:
        return []


def str_to_bool(val):
    return val.lower() in ('yes', 'true', 'on', '1')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('NETDASH_SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str_to_bool(os.getenv('NETDASH_DEBUG', 'off'))

ALLOWED_HOSTS = csv_to_list(os.getenv('NETDASH_ALLOWED_HOSTS', None))

CORS_ORIGIN_ALLOW_ALL = str_to_bool(os.getenv('NETDASH_CORS_ORIGIN_ALLOW_ALL', 'off'))

CORS_ORIGIN_WHITELIST = os.getenv('NETDASH_CORS_ORIGIN_WHITELIST', [])


NETDASH_MODULES = csv_to_list(os.getenv('NETDASH_MODULES'))

# Add all variables from the environment that start with NETDASH_ to the
# settings namespace, removing the leading "NETDASH_":
_prefix = 'NETDASH_APP_'
locals().update({k[len(_prefix):]: v for k, v in os.environ.items() if k[:len(_prefix)] == _prefix})

# Application definition

INSTALLED_APPS = NETDASH_MODULES + [
    'hostlookup_abstract',
    'netdash_api',
    'netdash_ui',
    'netdash',
    'rest_framework',
    'rest_framework_swagger',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'netdash.urls'
LOGIN_URL = os.getenv('NETDASH_LOGIN_URL', '/admin/login/')
AUTH_USER_MODEL = 'netdash.User'

_secure_proxy_ssl_header = os.getenv('NETDASH_SECURE_PROXY_SSL_HEADER', None)
if _secure_proxy_ssl_header:
    SECURE_PROXY_SSL_HEADER = (_secure_proxy_ssl_header, 'https')

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

WSGI_APPLICATION = 'netdash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('NETDASH_TIME_ZONE', 'America/Detroit')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

_saml2_entity_id = os.getenv('SAML2_ENTITY_ID', None)
_saml2_sp_name = os.getenv('SAML2_SP_NAME', None)
_saml2_sp_key = os.getenv('SAML2_SP_KEY', None)
_saml2_sp_cert = os.getenv('SAML2_SP_CERT', None)
_saml2_idp_metadata = os.getenv('SAML2_IDP_METADATA', None)
_saml2_acs_post = os.getenv('SAML2_ACS_POST', None)
_saml2_ls_redirect = os.getenv('SAML2_LS_REDIRECT', None)
_saml2_ls_post = os.getenv('SAML2_LS_POST', None)
_saml2_required_attributes = os.getenv('SAML2_REQUIRED_ATTRIBUTES', '').split(',')
_saml2_optional_attributes = os.getenv('SAML2_OPTIONAL_ATTRIBUTES', '').split(',')

if not (_saml2_sp_name and _saml2_sp_key and _saml2_sp_cert and _saml2_idp_metadata
        and _saml2_entity_id and _saml2_acs_post and _saml2_ls_post and _saml2_ls_redirect):
    print('SAML2 environment variables not set. Skipping djangosaml2 configuration.')
else:
    from .saml import create_saml_config
    import tempfile
    import json

    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/saml/login/'
    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS += ('djangosaml2.backends.Saml2Backend',)
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    # Generate temp files for cert, key, and metadata
    _sp_cert_file = tempfile.NamedTemporaryFile('w+', buffering=1)
    _sp_cert_file.write(_saml2_sp_cert + '\n')

    _sp_key_file = tempfile.NamedTemporaryFile('w+', buffering=1)
    _sp_key_file.write(_saml2_sp_key + '\n')

    _idp_metadata_file = tempfile.NamedTemporaryFile('w+', buffering=1)
    _idp_metadata_file.write(_saml2_idp_metadata + '\n')

    SAML_CONFIG = create_saml_config(_saml2_entity_id, _saml2_sp_name, _saml2_acs_post, _saml2_ls_redirect,
                                     _saml2_ls_post, _saml2_required_attributes, _saml2_optional_attributes,
                                     _sp_cert_file, _sp_key_file, _idp_metadata_file, DEBUG)
    SAML_CREATE_UNKNOWN_USER = True
    SAML_ATTRIBUTE_MAPPING = json.loads(os.getenv('SAML2_ATTRIBUTE_MAPPING', '{"uid": ["username"]}'))
