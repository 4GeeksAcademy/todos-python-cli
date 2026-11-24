# Lista de tareas CLI y API

Una aplicación modular de tareas con persistencia CSV y una interfaz FastAPI.

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta la aplicación de línea de comandos:

```bash
python main.py
```

Ejecuta el servidor FastAPI:

```bash
python server.py
```

La API estará disponible en `http://127.0.0.1:3000` y la documentación interactiva en `/docs`.

Los usuarios se guardan en `users.csv` y los todos se guardan en `todos.csv` con un `user_id`. Las rutas incluyen `/users`, `/users/{user_id}` y `/users/{user_id}/todos`. Los todos existentes se asignan al usuario predeterminado `id=1, username=default`.

## Requisitos

Asegúrate de tener Python instalado en tu computadora. Te recomendamos encarecidamente [instalar Python a través de Pyenv](https://4geeks.com/es/how-to/que-es-pyenv-y-como-instalar-pyenv) para evitar conflictos de versiones en el futuro.

### Contribuidores

Esta plantilla fue creada como parte de los [Recursos de Python de 4Geeks](https://4geeks.com/es/technology/python) para el aprendizaje en [4Geeks.com](https://4geeks.com) por [Alejandro Sanchez](https://twitter.com/alesanchezr) y [muchos otros contribuyentes](https://github.com/4GeeksAcademy/python-hello/graphs/contributors).
