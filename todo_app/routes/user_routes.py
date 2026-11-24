from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username):
        username = username.strip()
        if not username:
            raise ValueError("Username cannot be blank.")
        return username


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username):
        username = username.strip()
        if not username:
            raise ValueError("Username cannot be blank.")
        return username


class UserResponse(BaseModel):
    id: int
    username: str


def create_user_router(user_service, todo_service):
    router = APIRouter(prefix="/users", tags=["users"])

    def user_response(user):
        return UserResponse(id=user.id, username=user.username)

    @router.get("", response_model=list[UserResponse])
    def list_users():
        return [user_response(user) for user in user_service.list_users()]

    #/users
    @router.post("", response_model=UserResponse, status_code=201)
    def add_user(payload: UserCreate):
        try:
            return user_response(user_service.add(payload.username))
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    #/users/{user_id}
    #@app.get("/users/{user_id}", response_model=UserResponse)
    @router.get("/{user_id}", response_model=UserResponse)
    def get_user(user_id: int):
        try:
            return user_response(user_service.get(user_id))
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.put("/{user_id}", response_model=UserResponse)
    def update_user(user_id: int, payload: UserUpdate):
        try:
            return user_response(user_service.update(user_id, payload.username))
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.delete("/{user_id}", response_model=UserResponse)
    def delete_user(user_id: int):
        try:
            return user_response(user_service.delete(user_id, todo_service=todo_service))
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.get("/{user_id}/todos")
    def list_user_todos(user_id: int):
        from .todo_routes import TodoResponse

        try:
            return [
                TodoResponse(
                    title=todo.title,
                    priority=todo.priority,
                    is_done=todo.is_done,
                    user_id=todo.user_id,
                )
                for todo in todo_service.list_todos(user_id=user_id)
            ]
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    return router
