import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web import app  # noqa: E402


@pytest.fixture
def client():
    return app.test_client()
