from .base import *  # noqa

# Dev overrides
DEBUG = True

# Default to SQLite for dev unless DB_ENGINE explicitly set
if DB_ENGINE != "mysql":
    # DB config already set in base when DB_ENGINE == 'sqlite'
    pass

