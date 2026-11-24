from ..models.todo import Todo
from ..storage.todo_storage import load_todos, save_todos


class TodoService:
    def __init__(self, todos=None, user_service=None):
        self.todos = load_todos() if todos is None else todos
        self.user_service = user_service

    def list_todos(self, user_id=None):
        if user_id is None:
            return list(self.todos)
        self._validate_user(user_id)
        return [todo for todo in self.todos if todo.user_id == user_id]

    def add(self, title, priority, user_id=1):
        self._validate_user(user_id)
        todo = Todo(title, priority, user_id=user_id)
        self.todos.append(todo)
        save_todos(self.todos)
        return todo

    def get(self, position):
        return self.todos[self._index(position)]

    def update(self, position, title=None, priority=None, is_done=None, user_id=None):
        todo = self.todos[self._index(position)]
        if title is not None:
            todo.update_title(title)
        if priority is not None:
            todo.edit_priority(priority)
        if is_done is not None:
            if not isinstance(is_done, bool):
                raise ValueError("Todo completion state must be a boolean.")
            todo.is_done = is_done
        if user_id is not None:
            self._validate_user(user_id)
            todo.user_id = user_id
        save_todos(self.todos)
        return todo

    def toggle_done(self, position):
        todo = self.todos[self._index(position)]
        todo.toggle_done()
        save_todos(self.todos)
        return todo

    def delete(self, position):
        todo = self.todos.pop(self._index(position))
        save_todos(self.todos)
        return todo

    def _index(self, position):
        if not isinstance(position, int) or isinstance(position, bool):
            raise IndexError("Todo position must be an integer.")
        index = position - 1
        if index < 0 or index >= len(self.todos):
            raise IndexError("Todo position is out of range.")
        return index

    def _validate_user(self, user_id):
        if isinstance(user_id, bool) or not isinstance(user_id, int) or user_id < 1:
            raise ValueError("Todo user ID must be a positive integer.")
        if self.user_service is not None:
            try:
                self.user_service.get(user_id)
            except KeyError as error:
                raise ValueError("User not found.") from error
