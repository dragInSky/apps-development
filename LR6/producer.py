from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pika


@dataclass(frozen=True)
class ProductSeed:
    name: str
    price: float
    stock_quantity: int
    description: str | None = None


def _http_json(method: str, url: str, payload: dict | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        url=url,
        data=data,
        method=method.upper(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(req, timeout=5) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {url}: {body}") from e
    except URLError as e:
        raise RuntimeError(f"Cannot reach API {url}: {e}") from e


def _ensure_user(api_base_url: str, suffix: str) -> int:
    payload = {
        "email": f"rabbit_user_{suffix}@example.com",
        "username": f"rabbit_user_{suffix}",
        "first_name": "Rabbit",
        "last_name": "User",
    }
    user = _http_json("POST", f"{api_base_url}/users", payload)
    return int(user["id"])


def _wait_for_products(
    api_base_url: str, names: List[str], timeout_s: float = 20.0
) -> Dict[str, int]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        products = _http_json("GET", f"{api_base_url}/products") or []
        mapping = {p["name"]: int(p["id"]) for p in products if p.get("name") in names}
        if len(mapping) == len(names):
            return mapping
        time.sleep(0.5)
    raise TimeoutError("Products were not processed in time (check worker logs)")


def _publish_json(channel, queue: str, payload: dict) -> None:
    channel.queue_declare(queue=queue)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    )


def send_messages() -> None:
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    rabbit_host = os.getenv("RABBITMQ_HOST", "localhost")
    rabbit_port = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbit_vhost = os.getenv("RABBITMQ_VHOST", "local")

    suffix = uuid.uuid4().hex[:8]
    user_id = _ensure_user(api_base_url, suffix)

    products_seed: List[ProductSeed] = [
        ProductSeed(
            name=f"Laptop-{suffix}",
            price=1200.0,
            stock_quantity=5,
            description="Office laptop",
        ),
        ProductSeed(
            name=f"Mouse-{suffix}",
            price=25.5,
            stock_quantity=30,
            description="Wireless mouse",
        ),
        ProductSeed(
            name=f"Keyboard-{suffix}",
            price=55.0,
            stock_quantity=20,
            description="Mechanical keyboard",
        ),
        ProductSeed(
            name=f"Monitor-{suffix}",
            price=240.0,
            stock_quantity=10,
            description="24 inch display",
        ),
        ProductSeed(
            name=f"USB-C Cable-{suffix}",
            price=9.9,
            stock_quantity=50,
            description="1m cable",
        ),
    ]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbit_host, port=rabbit_port, virtual_host=rabbit_vhost
        )
    )
    channel = connection.channel()

    for product in products_seed:
        _publish_json(
            channel,
            "product",
            {
                "action": "create",
                "product": {
                    "name": product.name,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                    "description": product.description,
                },
            },
        )

    product_ids = _wait_for_products(api_base_url, [p.name for p in products_seed])

    orders = [
        {
            "user_id": user_id,
            "items": [
                {"product_id": product_ids[products_seed[0].name], "quantity": 1},
                {"product_id": product_ids[products_seed[1].name], "quantity": 2},
            ],
        },
        {
            "user_id": user_id,
            "items": [
                {"product_id": product_ids[products_seed[2].name], "quantity": 1},
                {"product_id": product_ids[products_seed[4].name], "quantity": 3},
            ],
        },
        {
            "user_id": user_id,
            "items": [
                {"product_id": product_ids[products_seed[3].name], "quantity": 1},
            ],
        },
    ]

    for order in orders:
        _publish_json(channel, "order", {"action": "create", "order": order})

    connection.close()

    created_products = _http_json("GET", f"{api_base_url}/products")
    created_orders = _http_json("GET", f"{api_base_url}/orders")
    print(f"Created user_id={user_id}")
    print(f"Products count={len(created_products or [])}")
    print(f"Orders count={len(created_orders or [])}")


if __name__ == "__main__":
    send_messages()
