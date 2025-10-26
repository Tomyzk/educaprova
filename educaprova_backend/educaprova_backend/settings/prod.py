from .base import *  # noqa

# Production overrides
DEBUG = False

# Ensure secure cookies in prod
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

