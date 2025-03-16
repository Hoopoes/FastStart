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
git clone --single-branch -b prisma-orm https://github.com/Hoopoes/FastStart.git
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
poetry shell
prisma generate
```

Alternatively, you can use Poetry to run Prisma commands:

```bash
poetry run prisma generate
```

6. Migrate Schema into SQL Database (Not for MongoDB)

This step is necessary when you first set up the database or when the schema has changed.

Run the following command to apply the schema migration to your SQL database:

```bash
prisma migrate dev --name <migration_name>
```

For the initial migration, you can use:

```bash
poetry shell
prisma migrate dev --name init
```

- If you need to alter the schema and migrate again, use:

```bash
poetry shell
prisma migrate dev --name <new_migration_name>
```

Alternatively, you can use Poetry to run Prisma commands:

```bash
poetry run prisma migrate dev --name <new_migration_name>
```

7. Apply Existing Migrations (if they have already been created)

If you already have migrations and just need to apply them (without generating new ones), you can use:
```bash
prisma migrate deploy
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
📦FastAPI-PrismaORM
 ┣ 📂app
 ┃ ┣ 📂api
 ┃ ┣ 📂db
 ┃ ┣ 📂job
 ┃ ┣ 📂middleware
 ┃ ┣ 📂models
 ┃ ┣ 📂res
 ┃ ┣ 📂schema
 ┃ ┣ 📂service
 ┃ ┣ 📂utils
 ┃ ┗ 🐍server.py
 ┣ 📂docs
 ┣ 📂logs
 ┣ 📂prisma
 ┣ 📂test
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
    - **job**: Background tasks, such as cron jobs or S3 bucket tasks.
    - **middleware**: Custom middleware implementations for request/response processing.
    - **models**: Machine Learning models.
    - **res**: Custom response handlers.
    - **schema**: Data validation schemas (using `pydantic`).
    - **service**: Business logic.
    - **utils**: Utility functions, such as a custom logger.
    - `server.py`: Sets up and configures the FastAPI server.

  - **docs**: Project documentation.

  - **logs**: Log files.

  - **prisma**: Prisma ORM files.
    - `partial_types.py`: Prisma partial types definitions.
    - `schema.prisma`: Prisma schema definitions.

  - **test**: Unit and integration tests.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **poetry.lock, pyproject.toml**: Dependency management.