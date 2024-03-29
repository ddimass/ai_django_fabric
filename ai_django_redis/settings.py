"""
Django settings for ai_django_redis project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

PAIRS_NEED = ("#ADS", "#BABA", "#AMZN", "#AAPL", "ASX200", "#BMW", "#BA", "BRENT", "CAC", "#EBAY", "#FB", "FDAX", "FTSE",
         "GOLD", "#GOOG", "HK50", "#BOS3", "IBEX35", "NED25", "#NFLX", "NI225", "#NIKE", "NQ", "SILVER", "SPX",
         "SWISS20", "SX5E", "#TSLA", "#TWTR", "USCRUDE", "#V", "#VOW", "YM", "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD",
         "AUDUSD", "BCHBTC", "BCHETH", "BCHUSD", "BTCUSD", "CADCHF", "CADJPY", "CHFJPY", "DSHBTC", "DSHUSD", "ETCBTC",
         "ETCUSD", "ETHBTC", "ETHLTC", "ETHUSD", "EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURPLN",
         "EURRUB", "EURTRY", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", "GBPDKK", "GBPJPY", "GBPNOK", "GBPNZD", "GBPSEK",
         "GBPTRY", "GBPUSD", "GBPZAR", "LTCBTC", "LTCUSD", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDCNH", "USDCZK",
         "USDDKK", "USDHUF", "USDILS", "USDJPY", "USDMXN", "USDNOK", "USDPLN", "USDRUB", "USDSEK", "USDSGD", "USDTRY",
         "USDZAR", "XAIUSD", "XMRBTC", "XMRUSD", "XPDUSD", "XPTUSD", "XRPUSD", "ZECBTC", "ZECUSD", "#AFKS", "#AFLT",
         "#BANE", "#BANEP", "#CHMF", "#FEES", "#GAZP", "#GMKN", "#HYDR", "#IRAO", "#LKOH", "#MAGN", "#MFON", "#MGNT",
         "#MOEX", "#MTSS", "#MVID", "#NLMK", "#NVTK", "#PHOR", "#PLZL", "#POLY", "#RASP", "#ROLO", "#ROSN", "#RSTI",
         "#RTKM", "#RUALR", "#SBER", "#SBERP", "#SIBN", "#SNGS", "#TATN", "#TATNP", "#TRNFP", "#UPRO", "#URKA",
         "#VTBR", "#YNDX", )
PAIRS = ("EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURPLN",
         "EURRUB", "EURTRY", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", "GBPDKK", "GBPJPY", "GBPNOK", "GBPNZD", "GBPSEK",
         "GBPTRY", "GBPUSD", "GBPZAR", "LTCBTC", "LTCUSD", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDCNH", "USDCZK",
         "USDDKK", "USDHUF", "USDILS", "USDJPY", "USDMXN", "USDNOK", "USDPLN", "USDRUB", "USDSEK", "USDSGD", "USDTRY",
         "USDZAR",)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h35q_uj7yk+*q7r9h76+^2hf*)i1o1thqv9t#=fto$t1f(!xgl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'nn.apps.NnConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'ai_django_redis.urls'

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

WSGI_APPLICATION = 'ai_django_redis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
CRONJOBS = [
    ('* * * * *', 'keras_ai.keras_model.index', '>> /usr/file.log')
]
