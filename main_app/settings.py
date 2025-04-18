"""
Django settings for main_app project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'vendor',
    'menu',
    'marketplace',
    'django.contrib.gis',
    'customers',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orders.request_object.RequestObjectMiddleware', # custom middleware created to acceess the request object in model.py
]

ROOT_URLCONF = 'main_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            # ทำหน้าที่เพิ่มข้อมูลให้กับ context ที่จะถูกส่งไปยังทุก template โดยอัตโนมัติ โดยไม่ต้องส่งข้อมูลซ้ำๆ ในทุก view
            # ทำให้ข้อมูลที่กำหนดปรากฏในทุกๆ template HTML ที่ถูก render โดยไม่ต้องส่งข้อมูลเหล่านี้ซ้ำๆ ในแต่ละ view
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.get_restaurant',
                'accounts.context_processors.get_google_api',
                'marketplace.context_processors.get_cart_counter',
                'marketplace.context_processors.get_cart_amounts',
                'accounts.context_processors.get_user_profile',
                'accounts.context_processors.get_paypal_client_id',
            ],
        },
    },
]

WSGI_APPLICATION = 'main_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),
        'USER' : config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
    }
}

AUTH_USER_MODEL = 'accounts.User'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'main_app/static'
]

# Media file configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# change error tag
MESSAGE_TAGS = {
    messages.ERROR: "danger"
}


# email configuration
EMAIL_HOST = config('EMAIL_HOST') # smtp server, 
EMAIL_PORT = config('EMAIL_PORT', cast=int) # 587 สำหรับ TLS หรือ 465 สำหรับ SSL
EMAIL_HOST_USER = config('EMAIL_HOST_USER') # actual email
EMAIL_HOST_PASSWORD = "icxxjtwimlyvppmr"
EMAIL_USE_TLS = True # เชื่อมต่อกับเซิร์ฟเวอร์ SMTP จะใช้ TLS
DEFAULT_FROM_EMAIL = "FoodOnline Admin <a64737287@gmail.com>"

# Google API key
GOOGLE_API_KEY = config('GOOGLE_API_KEY')

os.environ['PATH'] = os.path.join(BASE_DIR, 'env\\Lib\\site-packages\\osgeo') + ';' + os.environ['PATH']
os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'env\\Lib\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH']
GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, 'env\\Lib\\site-packages\\osgeo\\gdal.dll')

# Paypal client id
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')

# LinePay Channel ID and Channel Secret Key
LINEPAY_CHANNEL_ID = config('LINEPAY_CHANNEL_ID')
LINEPAY_SECRET_KEY = config('LINEPAY_SECRET_KEY')

# set CORS 
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'