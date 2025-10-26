import os
from django.core.wsgi import get_wsgi_application

# Prefer DJANGO_SETTINGS_MODULE if provided; default to production settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "educaprova_backend.settings.prod"),
)

application = get_wsgi_application()
