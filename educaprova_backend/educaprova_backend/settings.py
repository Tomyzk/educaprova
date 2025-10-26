"""
Compatibility wrapper: keep imports from the old settings path working.

Prefer using 'educaprova_backend.settings.dev' or 'educaprova_backend.settings.prod'.
"""

from .settings.dev import *  # noqa
