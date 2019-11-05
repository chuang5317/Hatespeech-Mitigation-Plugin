from http import HTTPStatus
import pytest

from flask import json
from backend import server

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


def test_get_method_returns_ok(client):
    response = client.get('/getmethod')
    assert response.status_code == HTTPStatus.OK, "HTTP request unsuccessful"
    data = json.loads(response.data)
    assert data == {"response": "OK"}
