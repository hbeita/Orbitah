# Orbitah API

A modular FastAPI backend for Orbitah, featuring user management, groups, goals, achievements, exploration state, and focus sessions. Built with SQLAlchemy ORM, Pydantic, JWT authentication, and full CRUD test coverage.

---

## Project Structure

```
orbitah-api/
  api/
    ├── __init__.py
    ├── main.py                # FastAPI api entrypoint
    ├── database.py            # SQLAlchemy setup (SQLite by default)
    ├── auth.py                # OAuth2/JWT authentication
    ├── models.py              # SQLAlchemy ORM models
    ├── schemas.py             # Pydantic schemas (request/response)
    ├── crud.py                # CRUD logic for all models
    └── routers/               # API routers (one per resource)
        ├── __init__.py
        ├── users.py
        ├── groups.py
        ├── goals.py
        ├── achievements.py
        ├── exploration.py
        └── focus_sessions.py
  tests/                       # Pytest-based test suite
    ├── test_achievements.py
    ├── test_exploration.py
    ├── test_goals.py
    ├── test_groups.py
    ├── test_users.py
    └── test_minimal_api.py
  requirements.txt             # Python dependencies
```

---

## Quickstart

### 1. Install dependencies (local dev)

```bash
cd orbitah-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the API (development)

```bash
uvicorn api.main:app --reload
```

- The API will be available at: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

### 3. Run the tests

```bash
PYTHONPATH=api pytest tests
```

---

## Docker

Build and run the API in a container:

```bash
docker build -t orbitah-api .
docker run -p 8000:8000 orbitah-api
```

---

## Docker Compose (with PostgreSQL)

A `docker-compose.yml` is provided to run both the API and a PostgreSQL database:

1. Create a `.env` file in `orbitah-api/` (see below).
2. Start everything:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at [http://localhost:8000](http://localhost:8000), and PostgreSQL at port 5432.

---

## Environment Variables

The app reads configuration from environment variables (see `.env`):

```
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://orbitah:orbitahpassword@db:5432/orbitahdb
SECRET_KEY=your-secret-key
```

- `SQLALCHEMY_DATABASE_URL`: Database connection string (PostgreSQL for Docker Compose, SQLite by default for local dev)
- `SECRET_KEY`: Secret key for JWT authentication

---

## API Overview

All endpoints are prefixed by their resource, e.g. `/users`, `/groups`, `/goals`, `/achievements`, `/exploration`, `/focus_sessions`.

Each resource supports standard CRUD operations:

- `POST /resource/` — Create
- `GET /resource/` — List
- `GET /resource/{id}` — Retrieve by ID
- `PUT /resource/{id}` — Update (fields optional)
- `DELETE /resource/{id}` — Delete

Example for users:
```http
POST    /users/           # Create a user
GET     /users/           # List users
GET     /users/{user_id}  # Get user by ID
PUT     /users/{user_id}  # Update user (fields optional)
DELETE  /users/{user_id}  # Delete user
```

Other routers follow the same pattern.

---

## Authentication

- OAuth2 password flow with JWT tokens.
- Endpoints for login and token generation are available (see `auth.py`).
- Secure endpoints require the `Authorization: Bearer <token>` header.

---

## Database

- Default: SQLite (`test.db` in project root).
- Change the connection string in `app/database.py` for production (e.g., PostgreSQL).

---

## Testing

- All CRUD operations are covered by tests in the `tests/` directory.
- Run tests with:
  ```bash
  PYTHONPATH=orbitah-api python3 -m pytest orbitah-api/tests | cat
  ```

---

## Dependencies

See `requirements.txt` for all dependencies. Key packages:
- fastapi
- uvicorn
- sqlalchemy
- alembic
- psycopg2-binary
- python-jose[cryptography]
- passlib[bcrypt]
- pydantic
- httpx
- pytest

---

## Notes & Tips

- All update endpoints accept partial updates (all fields optional).
- List fields in `ExplorationState` are stored as comma-separated strings in the DB, but exposed as lists in the API.
- Pydantic v2+ is used; schemas use `from_attributes = True` for ORM compatibility.
- For production, update the JWT `SECRET_KEY` in `auth.py` and use a secure database.

---

Let me know if you want to add usage examples, environment variable support, or deployment instructions!
