import csv
from pathlib import Path

from ..models.todo import Todo
from .user_storage import ensure_default_user


TODOS_FILE = Path(__file__).resolve().parent.parent.parent / "todos.csv"


def load_todos():
    ensure_default_user()
    try:
        with TODOS_FILE.open(newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))
    except FileNotFoundError:
        return []

    todos = []
    migrated = False
    for row_number, row in enumerate(rows, start=1):
        if len(row) not in (3, 4):
            raise ValueError(f"Invalid todo record on line {row_number} of {TODOS_FILE}")
        try:
            priority = int(row[1])
            if row[2] not in ("True", "False"):
                raise ValueError("completion state must be True or False")
            user_id = int(row[3]) if len(row) == 4 else 1
            todos.append(Todo(row[0], priority, row[2] == "True", user_id))
            migrated = migrated or len(row) == 3
        except ValueError as error:
            raise ValueError(
                f"Invalid todo record on line {row_number} of {TODOS_FILE}: {error}"
            ) from error
    if migrated:
        save_todos(todos)
    return todos


def save_todos(todos):
    with TODOS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(
            (todo.title, todo.priority, todo.is_done, todo.user_id) for todo in todos
        )
