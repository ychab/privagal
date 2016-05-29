import logging

from django.utils import six

from .base import *

DEBUG = True


SECRET_KEY = 'dev-dev-dev-dev'
PRIVAGAL_TIMELINE_INITIAL_PASSWORD = 'test'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

SENDFILE_BACKEND = 'sendfile.backends.development'

# Force every loggers to use console handler only. Note that using 'root'
# logger is not enough if children don't propage.
for logger in six.itervalues(LOGGING['loggers']):
    logger['handlers'] = ['console']
# Log every level.
LOGGING['handlers']['console']['level'] = logging.NOTSET

INTERNAL_IPS = ('127.0.0.1',)  # For debug toolbar

try:
    from .local import *
except ImportError:
    pass
