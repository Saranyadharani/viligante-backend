import os
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'temporary-secret-key-change-this-later')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'authentication',
    'auth_app',
    'scanner',
]

# SIMPLE POSTGRESQL CONFIG - NO SQLITE FALLBACK
DATABASES = {
    'default': dj_database_url.config()
}

# FIXED MIDDLEWARE - CORS MUST BE AT THE TOP!
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ADD THIS LINE AT THE TOP
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# CORS settings for frontend - UPDATED ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'viligante-backend-production.up.railway.app',
    'localhost',
    '127.0.0.1',
    '.railway.app'  # ADDED
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://127.0.0.1:3001", 
    "https://viligante-scanner-5406m46rf-saranyadharani84-3817s-projects.vercel.app",
    "https://viligante-scanner.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://viligante-scanner-5406m46rf-saranyadharani84-3817s-projects.vercel.app",
    "https://viligante-scanner.vercel.app",
    "https://viligante-backend-production.up.railway.app"  # ADDED
]

CORS_ALLOW_CREDENTIALS = True

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
