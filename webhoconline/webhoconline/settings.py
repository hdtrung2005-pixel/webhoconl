import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Tải file .env 
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-mac-dinh-neu-env-loi')


DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# --- CẤU HÌNH HỆ THỐNG  ---



INSTALLED_APPS = [
    'jazzmin', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'django.contrib.humanize',
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

# !!! FIX LỖI ATTRIBUTEERROR !!!
ROOT_URLCONF = 'webhoconline.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'app.context_processors.cart_count',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webhoconline.wsgi.application'

# CƠ SỞ DỮ LIỆU MSSQL
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'WebHocTap_Moi', 
        'USER': '', 
        'PASSWORD': '', 
        'HOST': r'DESKTOP-CU99I1G\SQLEXPRESS',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

# XÁC THỰC
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Múi giờ Việt Nam
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# TỆP TĨNH & MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'app.User'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

#Email OTP (Đọc từ .env)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') 

# VietQR (Đọc từ .env)
BANK_CODE = os.environ.get('BANK_CODE')
BANK_ACCOUNT_NUMBER = os.environ.get('BANK_ACCOUNT_NUMBER')
BANK_ACCOUNT_NAME = os.environ.get('BANK_ACCOUNT_NAME')

# JAZZMIN CONFIG
JAZZMIN_SETTINGS = {
    "site_title": "Admin Khóa học",
    "site_header": "Hệ Thống Quản Trị",
    "site_brand": "HỌC LẬP TRÌNH",
    "welcome_sign": "Chào mừng bạn quay lại!",
    "copyright": "Học Lập Trình - Phát triển bởi Trung",
    "show_version": False,
    "show_ui_builder": False, 
    "icons": {
        "auth.Group": "fas fa-users-cog",
        "app.User": "fas fa-user-graduate", 
        "app.Category": "fas fa-layer-group",
        "app.Course": "fas fa-book-open",
        "app.Lesson": "fas fa-play-circle",
        "app.Order": "fas fa-shopping-cart",
        "app.OrderItem": "fas fa-receipt",
        "app.Roadmap": "fas fa-map-signs",
        "app.LessonReview": "fas fa-star",
    },
    "usermenu_links": [
        {"name": "Quay về Trang chủ", "url": "/", "new_window": False, "icon": "fas fa-home"},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-white navbar-light",
    "font_family": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
    "theme": "litera",
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "accent": "accent-primary",
    "button_classes": {
        "primary": "btn-primary", "secondary": "btn-secondary", "info": "btn-info",
        "warning": "btn-warning", "danger": "btn-danger", "success": "btn-success"
    }
}