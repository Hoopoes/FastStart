# AGENTS.md

## Developer Setup
- Install `uv` (if not present): `pip install uv` or follow https://astral.sh/uv installation guide.
- Sync dependencies (incl. dev): `uv sync --all-groups`.
- Activate virtual environment (uv creates `.venv` automatically).
- Ensure `.env` is set up from `.env.example`.

## Quick Reference
- **Package manager**: `uv` — do not add Poetry config; `pyproject-poetry.toml` is a legacy leftover. Install all (incl. dev) via `uv sync --all-groups`.
- **Run**: `uv run python main.py [options]`
  - `--port <n>` (default 8000)
  - `--debug` (auto‑reload)
  - `-k <key.pem> -c <cert.pem>` (HTTPS)
  - `-w <n>` (uvicorn worker processes, default 1; do not combine with `--debug`)
- **Alt launch**: `uv run uvicorn app.server:app --host 0.0.0.0 --port 8000`
- **Lint/format**: `uv run ruff check .` / `uv run ruff format .`
- **Python**: `>=3.11,<3.13` (pyproject.toml)
- **Tests**: `uv run pytest` (async, in `tests/`; needs `uv sync --all-groups`)
- **Env copy  `.env.example` → `.env` fill secrets.


## Project Structure
```
📦 FastStart
├─ 📂app                     # Core FastAPI package
│   ├─ 📂auth                # JWT, password hashing, auth dependencies
│   ├─ 📂errors              # Custom errors & docs
│   ├─ 📂middlewares        # Middleware & exception handling
│   ├─ 📂models              # Pydantic models for API payloads (ORM models land here too)
│   ├─ 📂routes
│   │   ├─ 📂v1
│   │   │   ├─ 📂endpoints
│   │   │   │   └─ 🐍user.py          # User endpoint
│   │   │   └─ 🐍v1_route.py          # v1 router
│   │   └─ 🐍route.py                  # Root `/api` router
│   ├─ 📂schemas             # DTOs (`BaseResponseDto`, `CreateUserDto`)
│   ├─ 📂services           # Business logic
│   ├─ 📂utils               # Helpers (`logger.py`, `log_handler.py`, `config_loader.py`)
│   └─ 🐍server.py           # FastAPI app creation
├─ 🐍config.py               # Loads pyproject metadata & .env
├─ 🐍main.py                 # CLI – parses SSL/worker args, starts uvicorn
├─ 📜pyproject.toml          # uv manifest (dev group `ruff`)
├─ 📜pyproject-poetry.toml   # Legacy Poetry manifest (unused)
├─ 📜uv.lock                 # Lockfile
├─ 📜.env.example            # Template env (committed)
├─ 📜.env                    # Real env (git‑ignored)
├─ ⚙️logger.toml             # Logging config (level, format, context)
├─ 🤖AGENTS.md               # Guide for AI coding agents
├─ 📂tests                   # Async pytest suite
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
- `config.py` exposes `CONFIG` from `pyproject.toml` metadata (name, description, version) plus env: `ROOT_PATH` and the `AUTH_*` keys (`AUTH_SECRET_KEY`, `AUTH_ALGORITHM`, `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES`). Required keys have no default, so a missing value fails fast at import.
- `.env` loaded via `python-dotenv`; any key becomes runtime env var.
- `logger.toml` is loaded by `app/utils/config_loader.py` into `LOG_CONFIG`; controls log `level`, `format` (`json`/`logfmt`/`psv`), `indent`, and the `[context]` fields (`trace_id`, `endpoint`).
- `config.py` and `config_loader.py` resolve `pyproject.toml` and `logger.toml` by relative path, so run the app and tests from the project root.
- CLI args map straight to uvicorn params (`ssl_keyfile`, `ssl_certfile`, `workers`, `port`, `reload`).

## Conventions

The rules below are the starter's defaults. Extend or deviate when a real
requirement demands it, but move the rule here in the same change so the next
session reads the new truth instead of the old one.

- Routes under `app/routes/`; versioned APIs in `app/routes/v1/` (add `v2/` for breaking changes).
  Unversioned, cross-cutting endpoints (e.g. `auth.py`) live directly in `app/routes/` and are
  wired up by `app/routes/route.py`.
- Business logic in `app/services/`; import by handlers.
- **Auth package** – `app/auth/` is self-contained on purpose. It sits outside the versioned
  router (mounted at `/api/token`, not under `/api/v1`) and owns its own DTOs in
  `app/auth/models.py` (`Token`, `TokenData`, `UserAuth`) and its dependencies in
  `app/auth/dependencies.py` (`verify_access_token`, `require_admin`). Do **not** move those
  DTOs into `app/schemas/` and do **not** re-implement auth logic under `app/services/`.
  Auth flows that read or write user records call into `app/services/user_db.py`.
- **Schemas** – every versioned request/response DTO is a `pydantic.BaseModel` defined in
  `app/schemas/`. Import the model in the route; do **not** embed models inside route files.
  Documented exceptions: `app/auth/models.py` (see above) and `app/utils/config_loader.py`
  (infrastructure config models live next to the loader that owns them).
- **Error handling** – define new error subclasses in `app/errors/error.py`; import where needed.
  Do **not** raise raw `HTTPException` or create error classes elsewhere.
- **Authorization** – `Depends(verify_access_token)` for authenticated routes,
  `Depends(require_admin)` for admin-only ones. Identity is the email (JWT `sub`); the role is
  read from the user store on every request, so role changes take effect immediately.
- Middleware adds `X-Process-Time` header; logs each request (except harmless methods).
- Exception handling converts FastAPI/Starlette errors to `BaseResponseDto`.
- **Module visibility** – a `_`-prefixed name is private to its module. Promote it (drop the
  underscore) before importing it from anywhere else.
- **Testing** – cover new endpoints in `tests/`; `tests/conftest.py` provides the async `client`,
  token fixtures, and resets the in-memory store between tests.
- Run `ruff` and `pytest` before committing.

## Adding an Endpoint

1. **Schema** → `app/schemas/<domain>.py` (request DTO, response DTO, list wrapper).
2. **Errors** → new subclass in `app/errors/error.py` (never a raw `HTTPException`).
3. **Logic** → `app/services/<domain>.py`, or `<domain>_db.py` when it is store access.
4. **Route** → `app/routes/v1/endpoints/<domain>.py`, then register it in
   `app/routes/v1/v1_route.py` with a `prefix` and `tags`.
5. **Tests** → `tests/test_<domain>.py`, using the `client` and token fixtures.
6. **Config key?** → declare it in `.env.example` and add it to `ConfigClass` in `config.py`.
   Required keys have no default and fail fast at import.

Guard the new route with `Depends(verify_access_token)` or `Depends(require_admin)` unless it is
meant to be public, and keep the response shape consistent with the rest of the version.

*(End – concise, high‑signal guide for future sessions.)
