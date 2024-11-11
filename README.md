<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastAPI Base Project Structure

This repository's branch serves as a modular and flexible starting point for developing backend microservices with FastAPI.

## Prerequisites

Before setting up this project, ensure you have a basic understanding of the following tools:

- **[Poetry](https://python-poetry.org)**: Dependency management tool (like npm for Node.js).

- **[Pyenv](https://github.com/pyenv/pyenv)**: Manages multiple Python versions. For windows [pyenv-win](https://github.com/pyenv-win/pyenv-win).


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
📦FastAPI
 ┣ 📂app
 ┃ ┣ 📂api
 ┃ ┣ 📂job
 ┃ ┣ 📂middleware
 ┃ ┣ 📂models
 ┃ ┣ 📂response
 ┃ ┣ 📂schema
 ┃ ┣ 📂service
 ┃ ┣ 📂utils
 ┃ ┗ 🐍server.py
 ┣ 📂docs
 ┣ 📂logs
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
    - **job**: Background tasks, such as cron jobs or S3 bucket tasks.
    - **middleware**: Custom request/response handling.
    - **models**: Machine Learning models.
    - **response**: Custom response handlers.
    - **schema**: Data validation schemas (using `pydantic`).
    - **service**: Business logic.
    - **utils**: Utility functions, such as a custom logger.
    - `server.py`: Configures FastAPI server.

  - **docs**: Project documentation.

  - **logs**: Log files.

  - **test**: Unit and integration tests.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **poetry.lock, pyproject.toml**: Dependency management.