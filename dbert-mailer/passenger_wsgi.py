"""cPanel "Setup Python App" WSGI entry point. Passenger imports this module and
looks for a callable named `application`."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app import application  # noqa: E402
