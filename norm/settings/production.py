import dj_database_url
from common import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Salil Gupta', 'salil.gupta323@gmail.com'),
)

MANAGERS = ADMINS


DATABASES['default'] = dj_database_url.config()