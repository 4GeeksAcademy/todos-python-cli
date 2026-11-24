from ..models.user import User
from ..storage.user_storage import ensure_default_user, save_users


class UserService:
    def __init__(self, users=None):
        self.users = ensure_default_user() if users is None else users

    def list_users(self):
        return list(self.users)

    def add(self, username):
        user = User(self._next_id(), username)
        self._validate_unique_username(user.username)
        self.users.append(user)
        save_users(self.users)
        return user

    def get(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        raise KeyError("User not found.")

    def update(self, user_id, username):
        user = self.get(user_id)
        normalized = username.strip() if isinstance(username, str) else username
        if not isinstance(normalized, str) or not normalized:
            raise ValueError("Username cannot be blank.")
        self._validate_unique_username(normalized, excluding_id=user_id)
        user.update_username(normalized)
        save_users(self.users)
        return user

    def delete(self, user_id, todo_service=None):
        user = self.get(user_id)
        if todo_service is not None and any(
            todo.user_id == user_id for todo in todo_service.list_todos()
        ):
            raise ValueError("Cannot delete a user that owns todos.")
        self.users.remove(user)
        save_users(self.users)
        return user

    def _next_id(self):
        return max((user.id for user in self.users), default=0) + 1

    def _validate_unique_username(self, username, excluding_id=None):
        if any(
            user.username.lower() == username.lower() and user.id != excluding_id
            for user in self.users
        ):
            raise ValueError("Username already exists.")
