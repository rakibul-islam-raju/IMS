import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2gi5vzt084l1#kb-704@(!pl!$lha3v37bwt*psx=k4@283%$e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    # third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_filters',
    'django_seed',
    'import_export',

    # local
    'core',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ims.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ims.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nexbpthc_tafsir-inventory',
        'USER': 'nexbpthc_raju ',
        'PASSWORD': 'raju7772588RAJU',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC+6'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# all-auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


# allauth signup customization
ACCOUNT_FORMS = {'signup': 'core.forms.MyCustomSignupForm'}

AUTH_USER_MODEL = 'core.User'

# django-import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True

# email backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'rakibul-islam.nexbuzzy.com'
EMAIL_USE_TLS = False
EMAIL_PORT = 465 #This will be different based on your Host, for Namecheap I use this`
EMAIL_HOST_USER = 'dev@rakibul-islam.nexbuzzy.com' # Ex: info@pure.com
EMAIL_HOST_PASSWORD = 'raju7772588RAJU' # for the email you created through cPanel. The password for that

# if DEBUG:
#     EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = 'rakibul-islam.nexbuzzy.com '
#     EMAIL_USE_TLS = False
#     EMAIL_PORT = 465 #This will be different based on your Host, for Namecheap I use this`
#     EMAIL_HOST_USER = 'dev@rakibul-islam.nexbuzzy.com' # Ex: info@pure.com
#     EMAIL_HOST_PASSWORD = 'raju7772588RAJU' # for the email you created through cPanel. The password for that
# else:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
