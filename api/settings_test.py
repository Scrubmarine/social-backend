from backend.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_social_db',
        'USER': 'test_admin',
        'PASSWORD': 'testpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# You may also want to disable logging, enable Django's testing tools, etc.
DEBUG = True
TESTING = True