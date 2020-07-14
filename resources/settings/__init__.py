"""Django settings module initialize."""
import os

from .default import *  # noqa: F401

_APP_ENV = os.environ.get('APP_ENV', 'DEV')

if _APP_ENV == 'DEV':
    from .env_dev import *  # noqa: F401
elif _APP_ENV == 'STAG':
    from .env_stag import *  # noqa: F401
elif _APP_ENV == 'PROD':
    from .env_prod import *  # noqa: F401
elif _APP_ENV == 'TEST':
    from .env_test import *  # noqa: F401
