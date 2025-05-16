from .settings import *

# Use fast in-memory DB for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Faster password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Optional: simplify logging or disable it
LOGGING = {}