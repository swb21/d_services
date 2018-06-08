from .base import *

SECRET_KEY = 'p3ff8#fyqlh9l=nk=6$%e0otuk$apm@_3g%%eaaicpc=50!=66'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
