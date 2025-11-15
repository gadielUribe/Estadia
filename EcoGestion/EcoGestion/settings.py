import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-god5hezg+gr@o+sm!*z&-yhla9603z&^hhui*cx^(*)oq^usb4'

DEBUG = True

ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",") if h.strip()]

_csrf_env = [o.strip() for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS = list({
    *(_csrf_env or []),
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://192.168.1.123:8000",
    "http://187.214.167.93:8000",
})

INSTALLED_APPS = [
    "django_cleanup.apps.CleanupConfig",
    'usuario.apps.UsuarioConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plantas.apps.PlantasConfig',
    'respaldo.apps.RespaldoConfig',
    'chat.apps.ChatConfig',
    'herramientas.apps.HerramientasConfig',
    'productos.apps.ProductosConfig',
    'voluntarios.apps.VoluntariosConfig',
    'incidencias.apps.IncidenciasConfig',
    'salud.apps.SaludConfig',
    'notificaciones.apps.NotificacionesConfig',
    'calendario.apps.CalendarioConfig',
    'mantenimiento.apps.MantenimientoConfig',
    'reportes.apps.ReportesConfig',
    'channels',
    'dbbackup',
]

AUTH_USER_MODEL = 'usuario.Usuario'
ASGI_APPLICATION = 'EcoGestion.asgi.application'

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(REDIS_HOST, REDIS_PORT)]},
    }
}

AUTHENTICATION_BACKENDS = [
    'usuario.backends.MatriculaBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ASGI_APPLICATION = 'EcoGestion.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EcoGestion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notificaciones.context_processors.notificaciones_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'EcoGestion.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "EcoGest"),
        "USER": os.getenv("MYSQL_USER", "EcoUser"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "User_pass"),
        "HOST": os.getenv("MYSQL_HOST", "db"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
    }
}

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": BASE_DIR / "respaldo" / "backup"}
DBBACKUP_CLEANUP_KEEP = 5


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

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gadielvillaf@gmail.com'  
EMAIL_HOST_PASSWORD = 'dczd zcke bjzm vfhe'     
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Tiempo máximo de inactividad antes de cerrar sesión
SESSION_COOKIE_AGE = 1800  # 30 minutos en segundos
# Cerrar sesión al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

