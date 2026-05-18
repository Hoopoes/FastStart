# AGENTS.md

## Developer Setup
- Install `uv` (if not present): `pip install uv` or follow https://astral.sh/uv installation guide.
- Sync dependencies (incl. dev): `uv sync --all-groups`.
- Activate virtual environment (uv creates `.venv` automatically).
- Ensure `.env` is set up from `.env.example`.

## Quick Reference
- **Package manager**: `uv` (Poetry gone). Install all (incl. dev) via `uv sync --all-groups`.
- **Run**: `uv run python main.py [options]`
  - `--port <n>` (default 8000)
  - `--debug` (auto‑reload)
  - `-k <key.pem> -c <cert.pem>` (HTTPS)
- **Alt launch**: `uv run uvicorn app.server:app --host 0.0.0.0 --port 8000`
- **Lint/format**: `uv run ruff check .` / `uv run ruff format .`
- **Python >= 3.11 < 3.12` (pyproject.toml)
- **Tests none (removed) → 
- **Env copy  `.env.example` → `.env` fill secrets.


## Project Structure
```
📦 FastStart
├─ 📂app                     # Core FastAPI package
│   ├─ 📂errors              # Custom errors & docs
│   ├─ 📂middlewares        # Middleware & exception handling
│   ├─ 📂models              # Pydantic/ORM models (optional, DB classes)
│   ├─ 📂routes
│   │   ├─ 📂v1
│   │   │   ├─ 📂endpoints
│   │   │   │   └─ 🐍user.py          # User endpoint
│   │   │   └─ 🐍v1_route.py          # v1 router
│   │   └─ 🐍route.py                  # Root `/api` router
│   ├─ 📂schemas             # DTOs (`BaseResponseDto`, `CreateUserDto`)
│   ├─ 📂services           # Business logic
│   ├─ 📂utils               # Helpers (`logger.py`, `log_handler.py`)
│   └─ 🐍server.py           # FastAPI app creation
├─ 🐍config.py               # Loads pyproject metadata & .env
├─ 🐍main.py                 # CLI – parses SSL/worker args, starts uvicorn
├─ 📜pyproject.toml          # uv manifest (dev group `ruff`)
├─ 📜uv.lock                 # Lockfile
├─ 📜.env.example            # Template env (git‑ignored)
├─ 📜.env                    # Real env (git‑ignored)
└─ 📂docs                    # Docs assets (logo, etc.)
```

## Running Server
- **Standard** (no SSL):
  ```bash
  uv run python main.py --port 8000 --debug
  ```
- **SSL** (key & cert):
  ```bash
  uv run python main.py -k path/to/key.pem -c path/to/cert.pem --port 443
  ```
- **Direct uvicorn** (debug):
  ```bash
  uv run uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
  ```

## Config Details
- `config.py` reads `pyproject.toml` for name, description, version; pulls `ROOT_PATH` from env.
- `.env` loaded via `python-dotenv`; any key becomes runtime env var.
- CLI args map straight to uvicorn params (`ssl_keyfile`, `ssl_certfile`, `workers`, `port`, `reload`).

## Conventions
- Routes under `app/routes/`; versioned APIs in `app/routes/v1/` (add `v2/` for breaking changes).
- Business logic in `app/services/`; import by handlers.
- **Schemas** – every request/response DTO must be `pydantic.BaseModel` defined in `app/schemas/`. Import model in route; do **not** embed models inside route files.
- **Error handling** – define new error subclasses in `app/errors/error.py`; import where needed. Do **not** raise raw `HTTPException` or create error classes elsewhere.
- Middleware adds `X-Process-Time` header; logs each request (except harmless methods).
- Exception handling converts FastAPI/Starlette errors to `BaseResponseDto`.
- Run `ruff` before committing.

*(End – concise, high‑signal guide for future sessions.)
