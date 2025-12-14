from __future__ import annotations

import asyncio
import logging
import os

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from LR3.app.dependencies import async_session_factory, configure_engine, init_db
from LR3.app.schemas import OrderUpdate, ProductUpdate
from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.user_repository import UserRepository
from LR3.services.order_service import OrderService
from LR3.services.product_service import ProductService
from LR6.schemas import (
    OrderCreateMessage,
    OrderMessage,
    OrderUpdateStatusMessage,
    ProductCreateMessage,
    ProductMessage,
    ProductOutOfStockMessage,
    ProductUpdateMessage,
)

logger = logging.getLogger("lr6.worker")
_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, _level_name, logging.INFO))

broker = RabbitBroker(
    os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/local")
)
app = FastStream(broker)


@broker.subscriber("product")
async def subscribe_product(message: ProductMessage) -> None:
    async with async_session_factory() as session:
        product_service = ProductService(ProductRepository(session))

        if isinstance(message, ProductCreateMessage):
            product = await product_service.create(message.product)
            logger.info("product:create id=%s name=%s", product.id, product.name)
            return

        if isinstance(message, ProductUpdateMessage):
            product = await product_service.update(message.product_id, message.product)
            if not product:
                logger.warning(
                    "product:update not_found product_id=%s", message.product_id
                )
                return
            logger.info("product:update id=%s name=%s", product.id, product.name)
            return

        if isinstance(message, ProductOutOfStockMessage):
            product = await product_service.update(
                message.product_id, ProductUpdate(stock_quantity=0)
            )
            if not product:
                logger.warning(
                    "product:out_of_stock not_found product_id=%s", message.product_id
                )
                return
            logger.info("product:out_of_stock id=%s name=%s", product.id, product.name)
            return

        raise RuntimeError(f"Unsupported product message: {type(message)!r}")


@broker.subscriber("order")
async def subscribe_order(message: OrderMessage) -> None:
    async with async_session_factory() as session:
        order_service = OrderService(
            order_repository=OrderRepository(session),
            product_repository=ProductRepository(session),
            user_repository=UserRepository(session),
        )

        if isinstance(message, OrderCreateMessage):
            try:
                order = await order_service.create_order(message.order)
            except ValueError as exc:
                logger.warning(
                    "order:rejected reason=%s payload=%s",
                    exc,
                    message.model_dump(),
                )
                return
            logger.info("order:create id=%s user_id=%s", order.id, order.user_id)
            return

        if isinstance(message, OrderUpdateStatusMessage):
            order = await order_service.update(
                message.order_id, OrderUpdate(status=message.status)
            )
            if not order:
                logger.warning(
                    "order:update_status not_found order_id=%s", message.order_id
                )
                return
            logger.info("order:update_status id=%s status=%s", order.id, order.status)
            return

        raise RuntimeError(f"Unsupported order message: {type(message)!r}")


async def main() -> None:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        configure_engine(db_url)
    await init_db()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
