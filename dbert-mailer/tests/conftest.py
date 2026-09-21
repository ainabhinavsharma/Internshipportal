import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ["API_KEY"] = "test-api-key"
os.environ["DEFAULT_FROM_NAME"] = "DBERT Careers"
os.environ["DEFAULT_REPLY_TO"] = "careers@dbert.online"

import pytest

import app as mailer_module


@pytest.fixture()
def client():
    mailer_module.app.config["TESTING"] = True
    with mailer_module.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _reset_pool():
    mailer_module.pool._global_window.clear()
    for s in mailer_module.pool.senders:
        s.hourly_window.clear()
        s.daily_window.clear()
    yield
    mailer_module.pool._global_window.clear()
    for s in mailer_module.pool.senders:
        s.hourly_window.clear()
        s.daily_window.clear()
