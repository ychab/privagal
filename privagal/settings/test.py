import tempfile

from .base import *

SECRET_KEY = 'spam-spam-spam-spam'
PRIVAGAL_TIMELINE_INITIAL_PASSWORD = 'test'

MEDIA_ROOT = tempfile.gettempdir()

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SENDFILE_BACKEND = 'sendfile.backends.development'

# Boost perf a little
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

try:
    from .local import *
except ImportError:
    pass
