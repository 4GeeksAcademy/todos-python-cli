from dataclasses import dataclass


@dataclass
class Todo:
    title: str
    priority: int
    is_done: bool = False
    user_id: int = 1

    def __post_init__(self):
        self.update_title(self.title)
        self.edit_priority(self.priority)
        if not isinstance(self.is_done, bool):
            raise ValueError("Todo completion state must be a boolean.")
        if isinstance(self.user_id, bool) or not isinstance(self.user_id, int) or self.user_id < 1:
            raise ValueError("Todo user ID must be a positive integer.")

    def edit_priority(self, priority):
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 4:
            raise ValueError("Priority must be an integer from 1 to 4.")
        self.priority = priority

    def toggle_done(self):
        self.is_done = not self.is_done

    def update_title(self, title):
        if not isinstance(title, str):
            raise ValueError("Todo title must be a string.")
        title = title.strip()
        if not title:
            raise ValueError("Todo title cannot be blank.")
        self.title = title
