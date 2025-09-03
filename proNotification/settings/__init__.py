"""
Settings package for proNotification project.
This file imports the base settings and then tries to import environment-specific settings.
"""

from .base import *

# Try to import secret settings (for sensitive data)
try:
    from .secret import *
    print("Loaded secret settings")
except ImportError:
    print("Secret settings not found - using defaults")
    pass

# Try to import development settings (for local development)
try:
    from .development import *
    print("Loaded development settings")
except ImportError:
    pass

# Try to import production settings (for production deployment)
try:
    from .production import *
    print("Loaded production settings")
except ImportError:
    pass

# Try to import local settings (for machine-specific overrides)
try:
    from .local import *
    print("Loaded local settings")
except ImportError:
    pass
