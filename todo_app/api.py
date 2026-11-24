from fastapi import FastAPI

from .routes.todo_routes import create_todo_router
from .routes.user_routes import create_user_router
from .services.todo_service import TodoService
from .services.user_service import UserService


def create_app():
    app = FastAPI(title="Todo List API", version="1.0")
    user_service = UserService()
    todo_service = TodoService(user_service=user_service)

    app.include_router(create_user_router(user_service, todo_service))
    app.include_router(create_todo_router(todo_service, user_service))
    return app


app = create_app()
