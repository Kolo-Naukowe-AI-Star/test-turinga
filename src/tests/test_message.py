import pytest
from flask import Flask
from flask.testing import FlaskClient

from test_turinga import TuringServer


@pytest.fixture()
def turing_server():
    server = Flask(__name__)
    server.config.update(
        {
            "TESTING": True,
        }
    )
    server.register_blueprint(TuringServer())
    yield server


@pytest.fixture()
def client(turing_server: Flask):
    return turing_server.test_client()


def test_handshake(client: FlaskClient):
    response = client.get("/handshake")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert "id" in response.json
    assert isinstance(response.json["id"], str)


def test_retrieve_message(client: FlaskClient):
    handshake = client.get("/handshake")
    assert handshake.json
    id = handshake.json["id"]
    messages = client.get("/messages", headers={"X-User-ID": id})
    assert messages.json
    assert messages.status_code == 200
    assert not messages.json["messages"]


def test_receive_message(client: FlaskClient):
    handshake = client.get("/handshake")
    assert handshake.json
    id = handshake.json["id"]
    message = client.post(
        "/messages", headers={"X-User-ID": id}, data={"content": "Hello!"}
    )
    assert message.status_code == 400
    status = client.get("/status", headers={"X-User-ID": id})
    assert status.status_code == 200
    assert status.json
    assert status.json["ready"] == False
