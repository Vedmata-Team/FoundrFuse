import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foundrfuse.settings")

# This allows gunicorn to interface with Django's WSGI
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()