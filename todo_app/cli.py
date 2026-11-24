from .services.todo_service import TodoService
from .services.user_service import UserService


def display_todos(todos):
    if not todos:
        print("No todos yet.")
        return

    for position, todo in enumerate(todos, start=1):
        status = "Done" if todo.is_done else "Not done"
        print(f"{position}. {todo.title} (Priority: {todo.priority}, {status})")


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


def input_position(prompt):
    value = input(prompt).strip()
    try:
        return int(value)
    except ValueError:
        print("Enter a valid todo position.")
        return None


def add_todo(service, user_service):
    title = input("Todo title: ").strip()
    if not title:
        print("Todo title cannot be blank.")
        return
    priority = input_priority()
    if priority is None:
        return
    user_id = input_user_id(user_service)
    if user_id is None:
        return
    try:
        service.add(title, priority, user_id)
    except ValueError as error:
        print(error)
        return
    print("Todo added.")


def input_user_id(user_service):
    value = input("User ID: ").strip()
    try:
        user_id = int(value)
        user_service.get(user_id)
        return user_id
    except (ValueError, KeyError):
        print("Enter a valid existing user ID.")
        return None


def add_user(user_service):
    username = input("Username: ").strip()
    try:
        user = user_service.add(username)
    except ValueError as error:
        print(error)
        return
    print(f"User added: {user.username} (ID: {user.id})")


def delete_todo(service):
    todos = service.list_todos()
    display_todos(todos)
    if not todos:
        return
    position = input_position("Position to delete: ")
    if position is None:
        return
    try:
        deleted = service.delete(position)
    except IndexError:
        print("Todo position is out of range.")
        return
    print(f"Deleted: {deleted.title}")


def edit_todo(service):
    todos = service.list_todos()
    display_todos(todos)
    if not todos:
        return
    position = input_position("Position to edit: ")
    if position is None:
        return
    try:
        service.get(position)
    except IndexError:
        print("Todo position is out of range.")
        return

    print("1. Edit priority")
    print("2. Toggle done status")
    print("3. Update title")
    action = input("Choose an edit: ").strip()

    try:
        if action == "1":
            priority = input_priority()
            if priority is None:
                return
            service.update(position, priority=priority)
        elif action == "2":
            service.toggle_done(position)
        elif action == "3":
            title = input("New todo title: ").strip()
            if not title:
                print("Todo title cannot be blank.")
                return
            service.update(position, title=title)
        else:
            print("Choose an edit from 1 to 3.")
            return
    except ValueError as error:
        print(error)
        return
    print("Todo updated.")


def main():
    user_service = UserService()
    service = TodoService(user_service=user_service)

    while True:
        print("\nTodo List")
        print("1. Add todo")
        print("2. Show todos")
        print("3. Delete todo")
        print("4. Edit todo")
        print("5. Add user")
        print("6. List users")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_todo(service, user_service)
        elif choice == "2":
            display_todos(service.list_todos())
        elif choice == "3":
            delete_todo(service)
        elif choice == "4":
            edit_todo(service)
        elif choice == "5":
            add_user(user_service)
        elif choice == "6":
            users = user_service.list_users()
            if not users:
                print("No users yet.")
            for user in users:
                print(f"{user.id}. {user.username}")
        elif choice == "7":
            break
        else:
            print("Choose an option from 1 to 7.")

