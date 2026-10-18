<p align="center" width="100%">
  <img src="docs/fastapi.svg" alt="fastapi-logo" width="100">
</p>

# FastStart: A FastAPI Starter Kit
[![License](https://img.shields.io/github/license/Hoopoes/FastStart?style=flat-square&labelColor=343b41)](https://github.com/Hoopoes/FastStart/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/Hoopoes/FastStart?style=flat-square&labelColor=343b41)](https://github.com/Hoopoes/FastStart/stargazers)
[![Forks](https://img.shields.io/github/forks/Hoopoes/FastStart?style=flat-square&labelColor=343b41)](https://github.com/Hoopoes/FastStart/network/members)
[![Issues](https://img.shields.io/github/issues/Hoopoes/FastStart?style=flat-square&labelColor=343b41)](https://github.com/Hoopoes/FastStart/issues)
![Closed Issues](https://img.shields.io/github/issues-closed/Hoopoes/FastStart?style=flat-square&labelColor=343b41&color=blue)
[![Pull Requests](https://img.shields.io/github/issues-pr/Hoopoes/FastStart?style=flat-square&labelColor=343b41)](https://github.com/Hoopoes/FastStart/pulls)
[![Contributors](https://img.shields.io/github/contributors/Hoopoes/FastStart?style=flat-square&labelColor=343b41)](https://github.com/Hoopoes/FastStart/graphs/contributors)

**FastStart** is a modular and flexible starting point for building backend microservices with FastAPI. This repository provides a robust base structure with various extensions and configurations to help you get started quickly and efficiently.

## ✨ Features

- **Multiple Variations**: Different branches provide various features and integrations (see Branches table below).
- **Extensible**: Easily add and customize features as per your project requirements.
- **Best Practices**: Follow industry best practices for code organization, security, and performance.

## 🌱 Branches

| Branch Name                                                        | Description                                                                    |
|--------------------------------------------------------------------|--------------------------------------------------------------------------------|
| [main](https://github.com/Hoopoes/FastStart)       | A lightweight, stripped-down FastAPI starter with only essential boilerplate.     |
| [base](https://github.com/Hoopoes/FastStart/tree/base)             | Builds on `main` by adding improved OpenAPI documentation, better error handling, and common middleware utilities. |
| [sqlalchemy](https://github.com/Hoopoes/FastStart/tree/sqlalchemy) | Extends `base` with integrated support for Async SQLAlchemy to handle asynchronous database operations efficiently. |
| [log-viewer](https://github.com/Hoopoes/FastStart/tree/log-viewer) | Extends `base` with a built-in log viewer for inspecting application logs directly from the browser. |


## 📁 Branch Structure (`main`)

### 🚀 Getting Started

To get started with the FastAPI Starter Kit, follow the steps:

### Prerequisites

Before setting up this project, you should be familiar with:

- **[uv](https://docs.astral.sh/uv)**: A fast tool for managing Python packages, environments, and project dependencies.

### Setup

1. Clone the Repository

```bash
git clone --single-branch -b main https://github.com/Hoopoes/FastStart.git
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

### Project Structure

```
📦Project
 ┣ 📂app
 ┃ ┣ 📂auth
 ┃ ┣ 📂errors
 ┃ ┣ 📂middlewares
 ┃ ┣ 📂models
 ┃ ┣ 📂routes
 ┃ ┃ ┣ 🐍auth.py
 ┃ ┃ ┣ 🐍route.py
 ┃ ┃ ┣ 📂v1
 ┃ ┃ ┃ ┣ 📂endpoints
 ┃ ┃ ┃ ┃ ┗ 🐍user.py
 ┃ ┃ ┃ ┗ 🐍v1_route.py
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
 ┣ 🤖AGENTS.md
 ┣ ⚙️logger.toml
 ┣ 🐍config.py
 ┣ 🐍main.py
 ┣ 🔒uv.lock
 ┗ ⚙️pyproject.toml
```

### Explanation

- **Root Directory**: Configuration files and entry points.
  
  - **app**: Main application directory.
    - **auth**: JWT and OAuth2-based authentication helpers, token creation/validation, and demo user credential verification.
    - **errors**: Custom error response definitions, including error documentation for swagger.
    - **middlewares**: Custom middleware for request/response processing and exception handling.
    - **models**: Database models & core application objects.
    - **routes**: API endpoints and route handlers.
      - **auth.py** – Token issuance endpoint and authentication routes.
      - **v1** – Versioned API routes (e.g., v1). Additional versions like v2 or v3 can be created as needed for backward compatibility.
    - **schemas**: Data Transfer Objects (DTOs) & validation schemas (`pydantic`).
    - **services**: Business logic.
    - **utils**: Helper utilities for various tasks (e.g. logging).
    - `server.py`: Sets up and configures the FastAPI server.

  - **docs**: Project documentation.

  - **logs**: Log files.

  - **tests**: Async pytest suite covering authentication, user CRUD, and the admin-only authorization rules.

  - **.env**: Secret Environment configuration that is ignored by Git.

  - **.env.example**: Example environment configuration file that is not ignored by Git.

  - **AGENTS.md**: Guide for AI coding agents — setup, structure, and conventions.

  - **logger.toml**: Logging configuration read by `app/utils/config_loader.py` — level, output format (`json`/`logfmt`/`psv`), and the context fields added to every entry.

  - **config.py**: Project configurations, such as loading environment keys.

  - **main.py**: Application entry point.

  - **uv.lock, pyproject.toml**: Dependency management.

## Authentication

This starter includes a simple JWT-based authentication flow using FastAPI's OAuth2 password flow.

### Demo Credentials

- Email: `admin@example.com`
- Password: `admin123`
- Role: `admin`

Other demo users: `member@example.com` / `member123` (member), `inactive@example.com` / `member1234` (member, inactive). Inactive users cannot log in.

## 🧪 Tests

```bash
uv run pytest
```

## 📂 Log Viewer (in the `log-viewer` branch)

The [`log-viewer` branch](https://github.com/Hoopoes/FastStart/tree/log-viewer) adds a built-in log viewer for inspecting application logs directly from the browser.

![Logger Viewer](docs/log_viewer.png)

To access the Log Viewer, simply navigate to the appropriate route in the application (you may need to configure the path depending on your setup). This feature helps you monitor the logs and debug your application more effectively.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Hoopoes/FastStart&type=Timeline)](https://star-history.com/#Hoopoes/FastStart&Timeline)

## 📞 Contact

For any questions or feedback, please reach out to:
- Muhammad Umar Anzar - omer.anzar2@gmail.com

Or open an issue on GitHub.