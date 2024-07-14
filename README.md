<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI Base Project Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Setup

### Step 1: Clone Repo

```bash
git clone -b base https://github.com/Hoopoes/fastapi-starter-kit.git
```

### Step 2: Create Environment

Create a virtual environment using conda, pyenv, or any other tool, or simply install dependencies in your main Python environment.

- [**Conda**](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [**Pyenv**](https://github.com/pyenv/pyenv)

### Step 3: Install Poetry

First, install the Poetry package manager, which is similar to npm for Node.js.

```bash
pip install poetry
```
**For more guidance, visit the [Python Poetry Guide](https://python-poetry.org).**

### Step 4: Install Project Dependencies

To install all the packages listed in the `pyproject.toml` file, run:

```bash
poetry install
```

### Step 5: Generate Database Prisma Schema


Generate the Prisma schema:

```bash
prisma generate
```

OR

```bash
poetry run prisma generate
```

**For more guidance, visit the [Prisma Client Python Guide](https://prisma-client-py.readthedocs.io/en/stable/).**

### Step 6: Run `main.py`

Run the main application:

```bash
python main.py
```

OR

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
 ┃ ┗ 📜server.py
 ┣ 📂docs
 ┣ 📂logs
 ┣ 📂prisma
 ┣ 📂tests
 ┣ 📜.env
 ┣ 📜.env.example
 ┣ 📜.gitattributes
 ┣ 📜.gitignore
 ┣ 📜config.py
 ┣ 📜main.py
 ┣ 📜poetry.lock
 ┗ 📜pyproject.toml
```

### Explanation

- **Root Directory**: Contains project-wide configuration files and entry points.

  - **app**: Main application directory containing various modules and services.

    - **api**: Contains route handlers.
      - `user.py`: Defines API endpoints and their functions.
    
    - **db**: Database-related files.
      - `prisma_client.py`: Setup for Prisma client to interact with the database.
      - `user_db.py`: Database operations related to the user.
    
    - **jobs**: Scheduled jobs and background tasks.
      - Includes jobs like cron jobs or S3 bucket tasks.

    - **middlewares**: Custom middleware for request and response handling.
      - `usage.py`: Middleware to log and manage request usage statistics.
    
    - **models**: Machine Learning models.
      - `torch_.pt`: PyTorch model file.
      - `tf_.h5`: TensorFlow model file.
    
    - **responses**: Custom response handlers and structures.
      - `error.py`: Custom error responses.
    
    - **schemas**: Pydantic schemas for data validation and serialization.
      - `user_schema.py`: User-related schemas.
    
    - **services**: Business logic and service functions.
      - `user_service.py`: Contains complex functions used in API calls.
    
    - **utils**: Utility functions and helper modules.
      - `custom_log.py`: Custom logging setup.
      - `logger.py`: General logging functions.
    
    - `server.py`: Initializes and configures the FastAPI server.

  - **docs**: Project documentation files.

  - **logs**: Daily logs files.

  - **prisma**: Prisma ORM related files.
    - `partial_types.py`: Prisma partial types definitions.
    - `schema.prisma`: Prisma schema definitions.

  - **tests**: Unit and integration test files.

  - `.env`: Environment configuration file.
  - `.env.example`: Example environment configuration file that is not ignored by Git.
  - `.gitattributes`, `.gitignore`: Git configuration files to manage attributes and ignored files.
  - `config.py`: General project configurations, such as loading environment keys.
  - `main.py`: Entry point for the application.
  - `poetry.lock`, `pyproject.toml`: Dependency management files used by Poetry.
  - `README.md`: Documentation providing an overview and instructions for the project.