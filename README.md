<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI: Log Viewer Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Prerequisites

Before setting up this project, you should be familiar with:

- **[uv](https://docs.astral.sh/uv)**: A fast tool for managing Python packages, environments, and project dependencies.


## Setup

1. Clone the Repository

```bash
git clone --single-branch -b log-viewer https://github.com/Hoopoes/FastStart.git
cd FastStart
```

2. Install Dependencies

```bash
uv sync
```

3. Run the Application

```bash
uv run python main.py
```

## Project Structure

```
📦Project
 ┣ 📂app
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
 ┃ ┣ 📂templates
 ┃ ┣ 📂utils
 ┃ ┗ 🐍server.py
 ┣ 📂docs
 ┣ 📂logs
 ┣ 🗝️.env
 ┣ 🗝️.env.example
 ┣ 📜.gitattributes
 ┣ 📜.gitignore
 ┣ 🐍config.py
 ┣ 🐍main.py
 ┣ 🔒uv.lock
 ┗ ⚙️pyproject.toml
```

### Explanation

- **Root Directory**: Configuration files and entry points.
  
  - **app**: Main application directory.
    - **errors**: Custom error response definitions, including error documentation for swagger.
    - **middlewares**: Custom middleware for request/response processing and exception handling.
    - **models**: Database models & core application objects.
    - **routes**: API endpoints and route handlers.
      - **v1** – Versioned API routes (e.g., v1). Additional versions like v2 or v3 can be created as needed for backward compatibility.
    - **schemas**: Data Transfer Objects (DTOs) & validation schemas (`pydantic`).
    - **services**: Business logic.
    - **utils**: Helper utilities for various tasks (e.g. logging).
    - `server.py`: Sets up and configures the FastAPI server.

  - **docs**: Project documentation.

  - **logs**: Log files.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **uv.lock, pyproject.toml**: Dependency management.