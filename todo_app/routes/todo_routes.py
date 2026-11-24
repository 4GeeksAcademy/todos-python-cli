from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    priority: int = Field(ge=1, le=4)
    user_id: int = Field(default=1, ge=1)

    @field_validator("title")
    @classmethod
    def validate_title(cls, title):
        title = title.strip()
        if not title:
            raise ValueError("Todo title cannot be blank.")
        return title


class TodoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=4)
    is_done: Optional[bool] = None
    user_id: Optional[int] = Field(default=None, ge=1)

    @field_validator("title")
    @classmethod
    def validate_title(cls, title):
        if title is None:
            return title
        title = title.strip()
        if not title:
            raise ValueError("Todo title cannot be blank.")
        return title


class TodoResponse(BaseModel):
    title: str
    priority: int
    is_done: bool
    user_id: int


def create_todo_router(todo_service, user_service):
    router = APIRouter(prefix="/todos", tags=["todos"])

    def todo_response(todo):
        return TodoResponse(
            title=todo.title,
            priority=todo.priority,
            is_done=todo.is_done,
            user_id=todo.user_id,
        )

    @router.get("", response_model=list[TodoResponse])
    def list_todos():
        return [todo_response(todo) for todo in todo_service.list_todos()]

    @router.post("", response_model=TodoResponse, status_code=201)
    def add_todo(payload: TodoCreate):
        try:
            return todo_response(
                todo_service.add(payload.title, payload.priority, payload.user_id)
            )
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.get("/{position}", response_model=TodoResponse)
    def get_todo(position: int):
        try:
            return todo_response(todo_service.get(position))
        except IndexError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    #/todos/{position} PUT method
    @router.put("/{position}", response_model=TodoResponse)
    def update_todo(position: int, payload: TodoUpdate):
        try:
            return todo_response(
                todo_service.update(
                    position,
                    title=payload.title,
                    priority=payload.priority,
                    is_done=payload.is_done,
                    user_id=payload.user_id,
                )
            )
        except IndexError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.patch("/{position}/toggle", response_model=TodoResponse)
    def toggle_todo(position: int):
        try:
            return todo_response(todo_service.toggle_done(position))
        except IndexError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.delete("/{position}", response_model=TodoResponse)
    def delete_todo(position: int):
        try:
            return todo_response(todo_service.delete(position))
        except IndexError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    return router
