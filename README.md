# Todo List CLI and API

An interactive command-line todo list and FastAPI server. Todos are saved in `todos.csv`, and users are saved separately in `users.csv`, beside `main.py`.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the command-line application:

```bash
python main.py
```

Run the FastAPI server:

```bash
python server.py
```

The API is available at `http://127.0.0.1:3000`, with interactive documentation at `/docs`.

Use the menu to add, display, edit, or delete todos and create or list users. Todos require a `user_id`.

API routes include `/users`, `/users/{user_id}`, `/users/{user_id}/todos`, and `/todos`. Existing todos are migrated to the default user `id=1, username=default`.

## Requirements

Make sure you have Python installed. We recommend [installing Python through Pyenv](https://4geeks.com/how-to/what-is-pyenv-and-how-to-install-pyenv) to avoid version conflicts.

### Contributors

This template was built as part of the [4Geeks Python Resources](https://4geeks.com/technology/python) for learning at [4Geeks.com](https://4geeks.com) by [Alejandro Sanchez](https://twitter.com/alesanchezr) and [many other contributors](https://github.com/4GeeksAcademy/python-hello/graphs/contributors).
