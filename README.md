<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI Base Project Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Prerequisites

Before setting up this project, ensure you have a basic understanding of the following tools:

- **[Poetry](https://python-poetry.org)**: Dependency management tool (like npm for Node.js).

- **[Pyenv](https://github.com/pyenv/pyenv)**: Manages multiple Python versions. For windows [pyenv-win](https://github.com/pyenv-win/pyenv-win).

- **[Prisma](https://prisma-client-py.readthedocs.io/en/stable/)**: Object-Relational Mapper (ORM) for databases.


## Setup

1. Clone the Repository

```bash
git clone -b base https://github.com/Hoopoes/FastStart.git
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

5. Generate Database Prisma Schema

Generate the Prisma schema required for your project.

```bash
> poetry shell
> prisma generate
```

Alternatively, you can use Poetry to run Prisma commands:

```bash
poetry run prisma generate
```

1. Run `main.py`

Run the main application:

```bash
> poetry shell
> python main.py
```

Or, if you prefer to use Poetry:

```bash
poetry run python main.py
```


## Project Structure

```
📦FastAPI
 ┣ 📂app
 ┃ ┣ 📂api
 ┃ ┣ 📂db
 ┃ ┣ 📂jobs
 ┃ ┣ 📂middlewares
 ┃ ┣ 📂models
 ┃ ┣ 📂responses
 ┃ ┣ 📂schemas
 ┃ ┣ 📂services
 ┃ ┣ 📂utils
 ┃ ┗ 🐍server.py
 ┣ 📂docs
 ┣ 📂logs
 ┣ 📂prisma
 ┣ 📂tests
 ┣ 💾.env
 ┣ 💾.env.example
 ┣ 📜.gitattributes
 ┣ 📜.gitignore
 ┣ 🐍config.py
 ┣ 🐍main.py
 ┣ ⚙️poetry.lock
 ┗ ⚙️pyproject.toml
```

### Explanation

- **Root Directory**: Configuration files and entry points.
  
  - **app**: Main application directory.
    - **api**: Route handlers.
    - **db**: Database setup and operations.
    - **jobs**: Background tasks, such as cron jobs or S3 bucket tasks.
    - **middlewares**: Custom request/response handling.
    - **models**: Machine Learning models.
    - **responses**: Custom response handlers.
    - **schemas**: Data validation schemas (using `pydantic`).
    - **services**: Business logic.
    - **utils**: Utility functions, such as a custom logger.
    - `server.py`: Configures FastAPI server.

  - **docs**: Project documentation.

  - **logs**: Log files.

  - **prisma**: Prisma ORM files.
    - `partial_types.py`: Prisma partial types definitions.
    - `schema.prisma`: Prisma schema definitions.

  - **tests**: Unit and integration tests.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **poetry.lock, pyproject.toml**: Dependency management.