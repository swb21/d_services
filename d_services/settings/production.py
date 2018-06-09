from .base import *
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', '')

DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS.append('d-services.herokuapp.com')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
