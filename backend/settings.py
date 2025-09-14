import os  # ADD THIS LINE

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ADD THIS LINE

DEBUG = True
SECRET_KEY = 'temporary-secret-key-change-this-later'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # CORS headers
    'rest_framework',  # Django REST framework
    'authentication',
    'auth_app',
    'scanner',
]

# Use PostgreSQL for production (Railway automatically provides these env variables)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'db.sqlite3'),
        'USER': os.environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('RAILWAY_PRIVATE_DOMAIN', 'localhost'),
        'PORT': os.environ.get('PGPORT', '5432'),
    }
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

ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ADD THIS LINE

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ADD THESE LINES AT THE END:
# CORS settings for frontend
# Add your production frontend URL to CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://127.0.0.1:3001", 
    "https://viligante-scanner-5406m46rf-saranyadharani84-3817s-projects.vercel.app",  # ADD THIS
    "https://viligante-scanner.vercel.app",  # AND THIS
]
CSRF_TRUSTED_ORIGINS = [
    "https://viligante-scanner-5406m46rf-saranyadharani84-3817s-projects.vercel.app",
    "https://viligante-scanner.vercel.app",
]
CORS_ALLOW_CREDENTIALS = True

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}