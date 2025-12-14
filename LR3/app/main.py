from litestar import Litestar
from litestar.di import Provide

from LR3.app.dependencies import (
    init_db,
    provide_db_session,
    provide_order_repository,
    provide_order_service,
    provide_product_repository,
    provide_product_service,
    provide_user_repository,
    provide_user_service,
)
from LR3.controllers.order_controller import OrderController
from LR3.controllers.product_controller import ProductController
from LR3.controllers.user_controller import UserController


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[UserController, ProductController, OrderController],
        dependencies={
            "db_session": Provide(provide_db_session),
            "user_repository": Provide(provide_user_repository),
            "product_repository": Provide(provide_product_repository),
            "order_repository": Provide(provide_order_repository),
            "user_service": Provide(provide_user_service),
            "product_service": Provide(provide_product_service),
            "order_service": Provide(provide_order_service),
        },
        on_startup=[init_db],
    )


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
