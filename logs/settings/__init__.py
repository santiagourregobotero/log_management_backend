import os

ENVIRONTMENT = os.environ.get('DJANGO_ENV', 'dev')

if ENVIRONTMENT == 'production':
    from .production import *
else:
    from .dev import *
