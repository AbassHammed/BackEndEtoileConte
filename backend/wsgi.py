import os

from django.core.wsgi import get_wsgi_application

SETTINGS_MODULE = 'backeknd.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'backend.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)

application = get_wsgi_application()
