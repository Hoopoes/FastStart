<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI: Base Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Prerequisites

Before setting up this project, ensure you have a basic understanding of the following tools:

- **[Poetry](https://python-poetry.org)**: Dependency management tool (like npm for Node.js).

- **[Pyenv](https://github.com/pyenv/pyenv)**: Manages multiple Python versions. For windows [pyenv-win](https://github.com/pyenv-win/pyenv-win).


## Setup

1. Clone the Repository

```bash
git clone --single-branch -b base https://github.com/Hoopoes/FastStart.git
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

5. Run `main.py`

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
📦FastAPI-Base
 ┣ 📂app
 ┃ ┣ 📂core
 ┃ ┣ 📂errors
 ┃ ┣ 📂jobs
 ┃ ┣ 📂middleware
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
 ┣ 📂docs
 ┣ 📂logs
 ┣ 📂tests
 ┣ 🗝️.env
 ┣ 🗝️.env.example
 ┣ 📜.gitattributes
 ┣ 📜.gitignore
 ┣ 🐍config.py
 ┣ 🐍main.py
 ┣ 🔒poetry.lock
 ┗ ⚙️pyproject.toml
```

### Explanation

- **Root Directory**: Configuration files and entry points.
  
  - **app**: Main application directory.
    - **core**: Essential configurations (settings, logging, exception handling, authentication).
    - **errors**: Custom error response definitions, including error documentation for swagger.
    - **jobs**: Background tasks, such as cron jobs or S3 bucket tasks.
    - **middleware**: Custom middleware implementations for request/response processing.
    - **models**: Database models & core application objects.
    - **routes**: API endpoints and route handlers.
      - **v1** – Versioned API routes (e.g., v1). Additional versions like v2 or v3 can be created as needed for backward compatibility.
    - **schemas**: Data Transfer Objects (DTOs) & validation schemas (`pydantic`).
    - **services**: Business logic.
    - **utils**: Utility functions.
    - `server.py`: Sets up and configures the FastAPI server.

  - **docs**: Project documentation.

  - **logs**: Log files.

  - **tests**: Unit and integration tests.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **poetry.lock, pyproject.toml**: Dependency management.