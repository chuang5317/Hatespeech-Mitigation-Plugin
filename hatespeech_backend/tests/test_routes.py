
from http import HTTPStatus
import pytest

from flask import json
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


def test_get_method_returns_ok(client):
    response = client.get('/getmethod')
    assert response.status_code == HTTPStatus.OK, "HTTP request unsuccessful"
    data = json.loads(response.data)
    assert data == {"response": "OK"}


def test_post_method_returns_correct_result(client):
    nodes = [
        {"id": 1, "text": "hello there"},
        {"id": 2, "text": "now there are two of them"}
    ]
    response = client.post('/hatespeech', json={"nodes": nodes})
    assert response.status_code == HTTPStatus.OK, "HTTP request unsuccessful"
    result = json.loads(response.data)
    assert "result" in result, "Response missing 'result' field"
    assert len(nodes) == len(result["result"]), "Different number of values returned"
    for node, res in zip(nodes, result["result"]):
        assert node["id"] == res["id"]
        assert type(res["hatespeech"]) == bool
