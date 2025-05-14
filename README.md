<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI: Async SQLAlchemy Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Prerequisites

Before setting up this project, ensure you have a basic understanding of the following tools:

- **[Poetry](https://python-poetry.org)**: Dependency management tool (like npm for Node.js).

- **[Pyenv](https://github.com/pyenv/pyenv)**: Manages multiple Python versions. For windows [pyenv-win](https://github.com/pyenv-win/pyenv-win).

- **[Alembic](https://alembic.sqlalchemy.org)**: Lightweight database migration tool for SQLAlchemy.


## Setup

1. Clone the Repository

```bash
git clone --single-branch -b sqlalchemy https://github.com/Hoopoes/FastStart.git
```

2. Create a Virtual Environment (Optional)

Set up a Python virtual environment to manage your project’s dependencies independently. You can use a tool like pyenv or conda for this purpose

3. Install Poetry

```bash
pip install poetry
```

4. Install Project Dependencies

Install project's dependencies listed in the `pyproject.toml`.

```bash
poetry install
```

5. Initialize Alembic

(Optional) Skip this if the alembic/ folder already exists

```bash
poetry shell
alembic init -t async alembic
```
This creates the `alembic` folder and a preconfigured async-compatible `env.py`.


6. Create and Apply Initial Migration

Edit `alembic/env.py` to import your models and use the correct `SQLALCHEMY_DATABASE_URL` from your settings.

```bash
# Create initial migration from SQLAlchemy models
alembic revision --autogenerate -m "Initial tables"
```


7. Apply Existing Migrations

If you already have migrations and just need to apply them (without generating new ones), you can use:
```bash
alembic upgrade head
```
This will apply any pending migrations to your SQL database.


8. Run `main.py`

Run the main application:

```bash
poetry shell
python main.py
```

Or, if you prefer to use Poetry:

```bash
poetry run python main.py
```


## Project Structure

```
📦FastAPI-SQLAlchemy
 ┣ 📂app
 ┃ ┣ 📂db
 ┃ ┣ 📂errors
 ┃ ┣ 📂middlewares
 ┃ ┣ 📂models
 ┃ ┣ 📂routes
 ┃ ┃ ┣ 📂v1
 ┃ ┃ ┃ ┣ 📂endpoints
 ┃ ┃ ┃ ┃ ┗ 🐍user.py
 ┃ ┃ ┃ ┗ 🐍v1_route.py
 ┃ ┃ ┗ 🐍route.py
 ┃ ┣ 📂schemas
 ┃ ┣ 📂services
 ┃ ┣ 📂utils
 ┃ ┗ 🐍server.py
 ┣ 📂db
 ┣ 📂docs
 ┣ 📂logs
 ┣ 📂alembic
 ┣ 🗝️.env
 ┣ 🗝️.env.example
 ┣ 📜.gitattributes
 ┣ 📜.gitignore
 ┣ 📜alembic.ini
 ┣ 🐍config.py
 ┣ 🐍main.py
 ┣ 🔒poetry.lock
 ┗ ⚙️pyproject.toml
```

### Explanation

- **Root Directory**: Configuration files and entry points.
  
  - **app**: Main application directory.
    - **db**: Database configuration and connection setup (e.g. engine, session, initialization).
    - **errors**: Custom error response definitions, including error documentation for swagger.
    - **middlewares**: Custom middleware for request/response processing and exception handling.
    - **models**: Database models & core application objects.
    - **routes**: API endpoints and route handlers.
      - **v1** – Versioned API routes (e.g., v1). Additional versions like v2 or v3 can be created as needed for backward compatibility.
    - **schemas**: Data Transfer Objects (DTOs) & validation schemas (`pydantic`).
    - **services**: Business logic.
    - **utils**: Helper utilities for various tasks (e.g. logging).
    - `server.py`: Sets up and configures the FastAPI server.
  
  - **db**: Local SQLite database that is ignored by Git.
  
  - **docs**: Project documentation.

  - **logs**: Log files.

  - **alembic**: Alembic Migrations files.
    - `env.py`: Configures DB connection and runs migrations.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **alembic.ini**: Alembic config file for database connection, migration paths, and settings.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **poetry.lock, pyproject.toml**: Dependency management.