import pytest
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED


def test_user_endpoints(client):
    payload = {
        "email": "alexander.test@gmail.com",
        "username": "alex_test",
        "first_name": "Alexander",
        "last_name": "Testov",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == HTTP_201_CREATED

    user_id = response.json()["id"]

    response = client.get("/users")
    assert response.status_code == HTTP_200_OK
    assert any(user["id"] == user_id for user in response.json())

    response = client.put(f"/users/{user_id}", json={"first_name": "Alex"})
    assert response.status_code == HTTP_200_OK
    assert response.json()["first_name"] == "Alex"

    response = client.delete(f"/users/{user_id}")
    assert response.status_code in (HTTP_200_OK, 204)


def test_product_endpoints(client):
    response = client.post(
        "/products",
        json={"name": "Backpack", "price": 39.9, "stock_quantity": 25},
    )
    assert response.status_code == HTTP_201_CREATED
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == HTTP_200_OK
    assert response.json()["name"] == "Backpack"

    response = client.put(
        f"/products/{product_id}",
        json={"stock_quantity": 19},
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["stock_quantity"] == 19

    response = client.delete(f"/products/{product_id}")
    assert response.status_code in (HTTP_200_OK, 204)


def test_order_endpoints(client):
    user_id = client.post(
        "/users",
        json={
            "email": "order.person@gmail.com",
            "username": "order_person",
            "first_name": "Olga",
            "last_name": "Sidorova",
        },
    ).json()["id"]

    product1 = client.post(
        "/products",
        json={"name": "Desk Lamp", "price": 42.5, "stock_quantity": 4},
    ).json()
    product2 = client.post(
        "/products",
        json={"name": "Notebook", "price": 6.2, "stock_quantity": 12},
    ).json()

    order_payload = {
        "user_id": user_id,
        "items": [
            {"product_id": product1["id"], "quantity": 1},
            {"product_id": product2["id"], "quantity": 2},
        ],
    }

    response = client.post("/orders", json=order_payload)
    assert response.status_code == HTTP_201_CREATED

    order = response.json()
    assert len(order["items"]) == 2
    assert order["total_amount"] == pytest.approx(42.5 * 1 + 6.2 * 2)

    response = client.get(f"/orders/{order['id']}")
    assert response.status_code == HTTP_200_OK

    response = client.put(f"/orders/{order['id']}", json={"status": "paid"})
    assert response.status_code == HTTP_200_OK
    assert response.json()["status"] == "paid"

    response = client.delete(f"/orders/{order['id']}")
    assert response.status_code in (HTTP_200_OK, 204)
