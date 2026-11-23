import csv
from pathlib import Path


TODOS_FILE = Path(__file__).with_name("todos.csv")


class Todo:
    def __init__(self, title, priority, is_done=False):
        self.update_title(title)
        self.edit_priority(priority)
        if not isinstance(is_done, bool):
            raise ValueError("Todo completion state must be a boolean.")
        self.is_done = is_done

    def edit_priority(self, priority):
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 4:
            raise ValueError("Priority must be an integer from 1 to 4.")
        self.priority = priority

    def toggle_done(self):
        self.is_done = not self.is_done

    def update_title(self, title):
        title = title.strip()
        if not title:
            raise ValueError("Todo title cannot be blank.")
        self.title = title


def load_todos():
    try:
        with TODOS_FILE.open(newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))
    except FileNotFoundError:
        return []

    todos = []
    for row_number, row in enumerate(rows, start=1):
        if len(row) != 3:
            raise ValueError(f"Invalid todo record on line {row_number} of {TODOS_FILE}")
        try:
            priority = int(row[1])
            if row[2] not in ("True", "False"):
                raise ValueError("completion state must be True or False")
            todos.append(Todo(row[0], priority, row[2] == "True"))
        except ValueError as error:
            raise ValueError(
                f"Invalid todo record on line {row_number} of {TODOS_FILE}: {error}"
            ) from error
    return todos


def save_todos(todos):
    with TODOS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(
            (todo.title, todo.priority, todo.is_done) for todo in todos
        )


def display_todos(todos):
    if not todos:
        print("No todos yet.")
        return

    for position, todo in enumerate(todos, start=1):
        status = "Done" if todo.is_done else "Not done"
        print(f"{position}. {todo.title} (Priority: {todo.priority}, {status})")


def add_todo(todos):
    title = input("Todo title: ").strip()
    if not title:
        print("Todo title cannot be blank.")
        return
    priority = input_priority()
    if priority is None:
        return
    todos.append(Todo(title, priority))
    save_todos(todos)
    print("Todo added.")


def input_priority():
    value = input("Priority (1-4, 1 is highest): ").strip()
    try:
        priority = int(value)
        if not 1 <= priority <= 4:
            raise ValueError
    except ValueError:
        print("Priority must be an integer from 1 to 4.")
        return None
    return priority


def delete_todo(todos):
    display_todos(todos)
    if not todos:
        return
    position = input("Position to delete: ").strip()
    try:
        index = int(position) - 1
    except ValueError:
        print("Enter a valid todo position.")
        return
    if index < 0 or index >= len(todos):
        print("Todo position is out of range.")
        return
    deleted = todos.pop(index)
    save_todos(todos)
    print(f"Deleted: {deleted.title}")


def edit_todo(todos):
    display_todos(todos)
    if not todos:
        return
    position = input("Position to edit: ").strip()
    try:
        index = int(position) - 1
    except ValueError:
        print("Enter a valid todo position.")
        return
    if index < 0 or index >= len(todos):
        print("Todo position is out of range.")
        return

    todo = todos[index]
    print("1. Edit priority")
    print("2. Toggle done status")
    print("3. Update title")
    action = input("Choose an edit: ").strip()

    if action == "1":
        priority = input_priority()
        if priority is None:
            return
        todo.edit_priority(priority)
    elif action == "2":
        todo.toggle_done()
    elif action == "3":
        title = input("New todo title: ").strip()
        if not title:
            print("Todo title cannot be blank.")
            return
        todo.update_title(title)
    else:
        print("Choose an edit from 1 to 3.")
        return

    save_todos(todos)
    print("Todo updated.")


def main():
    todos = load_todos()

    while True:
        print("\nTodo List")
        print("1. Add todo")
        print("2. Show todos")
        print("3. Delete todo")
        print("4. Edit todo")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_todo(todos)
        elif choice == "2":
            display_todos(todos)
        elif choice == "3":
            delete_todo(todos)
        elif choice == "4":
            edit_todo(todos)
        elif choice == "5":
            break
        else:
            print("Choose an option from 1 to 5.")


if __name__ == "__main__":
    main()
