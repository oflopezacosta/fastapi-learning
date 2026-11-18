
from fastapi.testclient import TestClient
from main import app
import pytest
from main import items, Item

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_items():
    items.clear()
    items.extend([
        Item(text="apple", is_done=False),
        Item(text="banana", is_done=True),
        Item(text="orange", is_done=False)
    ])


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_get_items():
    response = client.get("/items")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_item_not_found():
    response = client.get("/items/999")

    assert response.status_code == 404


def test_create_item():
    response = client.post(
        "/items",
        json={"text": "grape", "is_done": False}
    )

    assert response.status_code == 201
    assert response.json()["text"] == "grape"


def test_update_item():
    response = client.patch(
        "/items/0",
        json={"text": "grape"}
    )

    assert response.status_code == 200
    assert response.json()["text"] == "grape"
    assert response.json()["is_done"] == False


def test_delete_item():
    before = client.get("/items/0").json()

    response = client.delete("/items/0")

    assert response.status_code == 200
    assert response.json()["deleted_item"] == before


def test_update_item_not_found():
    response = client.patch(
        "/items/999",
        json={"text": "grape"}
    )

    assert response.status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/999")

    assert response.status_code == 404

