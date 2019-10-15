
from http import HTTPStatus
import pytest

from hatespeech_backend import server


@pytest.fixture
def client():
    """Create a simple test interface to the server."""
    client = server.app.test_client()
    yield client


def test_root_returns_greeting(client):
    """Check that calling the root returns the "Hello World" message."""
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK, "HTTP request unsuccessful"
    assert response.data == b"Hello, World!"
