import csv
from pathlib import Path

from ..models.user import User


USERS_FILE = Path(__file__).resolve().parent.parent.parent / "users.csv"


def load_users():
    try:
        with USERS_FILE.open(newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))
    except FileNotFoundError:
        rows = []

    users = []
    for row_number, row in enumerate(rows, start=1):
        if len(row) != 2:
            raise ValueError(f"Invalid user record on line {row_number} of {USERS_FILE}")
        try:
            users.append(User(int(row[0]), row[1]))
        except ValueError as error:
            raise ValueError(
                f"Invalid user record on line {row_number} of {USERS_FILE}: {error}"
            ) from error
    return users


def save_users(users):
    with USERS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows((user.id, user.username) for user in users)


def ensure_default_user():
    users = load_users()
    if not users:
        users = [User(1, "default")]
        save_users(users)
    elif not any(user.id == 1 for user in users):
        users.insert(0, User(1, "default"))
        save_users(users)
    return users
