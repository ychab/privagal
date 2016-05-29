from .base import *

DEBUG = False

SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True

# See https://github.com/johnsensible/django-sendfile/blob/v0.3.10/README.rst
SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = MEDIA_ROOT
SENDFILE_URL = '/protected/'

try:
    from .local import *
except ImportError:
    pass
