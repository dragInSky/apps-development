from litestar import Litestar
from litestar.di import Provide
from LR3.app.dependencies import provide_user_service, provide_user_repository, provide_db_session
from LR3.controllers.user_controller import UserController

app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
