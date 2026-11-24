from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str

    def __post_init__(self):
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id < 1:
            raise ValueError("User ID must be a positive integer.")
        self.update_username(self.username)

    def update_username(self, username):
        if not isinstance(username, str):
            raise ValueError("Username must be a string.")
        username = username.strip()
        if not username:
            raise ValueError("Username cannot be blank.")
        self.username = username
