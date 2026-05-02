<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI: Async SQLAlchemy Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Prerequisites

Before setting up this project, you should be familiar with:

- **[uv](https://docs.astral.sh/uv)**: A fast tool for managing Python packages, environments, and project dependencies.

- **[Alembic](https://alembic.sqlalchemy.org)**: Lightweight database migration tool for SQLAlchemy.


## Setup

1. Clone the Repository

```bash
git clone --single-branch -b sqlalchemy https://github.com/Hoopoes/FastStart.git
cd FastStart
```

2. Install Dependencies

```bash
uv sync
```

3. Initialize Alembic

(Optional) Skip this if the alembic/ folder already exists

```bash
uv run alembic init -t async alembic
```
This creates the `alembic` folder and a preconfigured async-compatible `env.py`.


4. Create and Apply Initial Migration

Edit `alembic/env.py` to import your models and use the correct `SQLALCHEMY_DATABASE_URL` from your settings.

```bash
# Create initial migration from SQLAlchemy models
uv run alembic revision --autogenerate -m "Initial tables"
```

5. Apply Existing Migrations

If you already have migrations and just need to apply them (without generating new ones), you can use:
```bash
uv run alembic upgrade head
```
This will apply any pending migrations to your SQL database.

6. Run the Application

```bash
uv run python main.py
```

## Project Structure

```
📦Project
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
 ┣ 🔒uv.lock
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

  - **uv.lock, pyproject.toml**: Dependency management.