import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ["API_KEY"] = "test-api-key"
os.environ["ALLOWED_SENDER_DOMAINS"] = "dbert.info,dbert.online"
os.environ["DEFAULT_FROM_EMAIL"] = "careers@dbert.info"
os.environ["DEFAULT_FROM_NAME"] = "DBERT Careers"
os.environ["RATE_LIMIT_PER_MIN"] = "1000"  # high enough that tests don't trip it

import pytest

import app as mailer_module


@pytest.fixture()
def client():
    mailer_module.app.config["TESTING"] = True
    with mailer_module.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _reset_rate_window():
    mailer_module._rate_window.clear()
    yield
    mailer_module._rate_window.clear()
