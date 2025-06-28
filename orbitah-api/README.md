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
3. The API will be available at [http://localhost:8001](http://localhost:8001), and PostgreSQL at port 5433.

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

The project includes a comprehensive test suite with **35 tests** across 7 test files, covering all CRUD operations, authentication, and authorization.

### Test Coverage

- **test_auth.py** (14 tests) - OAuth2/JWT authentication, user registration, login, token validation
- **test_users.py** (4 tests) - User CRUD operations with authentication
- **test_goals.py** (4 tests) - Goal CRUD operations
- **test_groups.py** (4 tests) - Group CRUD operations
- **test_exploration.py** (4 tests) - Exploration state CRUD operations
- **test_achievements.py** (3 tests) - Achievement CRUD operations
- **test_minimal_api.py** (2 tests) - Basic API health checks

### Running All Tests

#### Option 1: Using PostgreSQL (Recommended)
Run all tests together using the PostgreSQL database:

```bash
cd orbitah-api
# Start Docker Compose first
docker compose up -d

# Run tests with PostgreSQL
PYTHONPATH=. python3 -m pytest tests/ -v
```

#### Option 2: Using the Test Runner Script
The test runner script runs each test file in isolation to avoid database conflicts:

```bash
cd orbitah-api
python3 run_tests.py
```

This will:
- Run each test file separately
- Clean up database files between tests
- Provide a summary of results
- Show ✅ for passed tests and ❌ for failed tests

#### Option 3: Using Pytest with SQLite
Run all tests at once with SQLite (may have database conflicts):

```bash
cd orbitah-api
PYTHONPATH=. python3 -m pytest tests/ -v
```

### Running Individual Test Files

Run a specific test file:

```bash
cd orbitah-api
# With PostgreSQL
PYTHONPATH=. python3 -m pytest tests/test_auth.py -v

# With SQLite
PYTHONPATH=. python3 -m pytest tests/test_auth.py -v
```

### Running Specific Tests

Run a specific test function:

```bash
cd orbitah-api
PYTHONPATH=. python3 -m pytest tests/test_auth.py::test_register_user -v
PYTHONPATH=. python3 -m pytest tests/test_users.py::test_create_user -v
```

### Test Output Examples

#### Successful Test Run
```
Running tests in isolation to avoid database conflicts...
============================================================

Running tests/test_auth.py...
✅ tests/test_auth.py - PASSED

Running tests/test_users.py...
✅ tests/test_users.py - PASSED

============================================================
SUMMARY: 7 passed, 0 failed
🎉 All tests passed!
```

#### Individual Test File
```
============================================== test session starts ===============================================
platform darwin -- Python 3.11.3, pytest-8.4.1, pluggy-1.6.0
collected 14 items

test_register_user PASSED                                                  [  7%]
test_register_duplicate_user PASSED                                        [ 14%]
test_login_success PASSED                                                  [ 21%]
...
test_token_expiration PASSED                                               [100%]

========================================= 14 passed, 9 warnings in 4.20s =========================================
```

### Test Database

- **PostgreSQL**: Tests use the same PostgreSQL database as the application (port 5433)
- **SQLite**: Tests use SQLite databases with unique names to avoid conflicts
- Database files are automatically cleaned up between test runs
- Each test runs in its own transaction that gets rolled back

### Troubleshooting

If you encounter database conflicts when running all tests together:
1. Use PostgreSQL: `docker compose up -d && PYTHONPATH=. python3 -m pytest tests/ -v`
2. Use the test runner script: `python3 run_tests.py`
3. Or run individual test files separately
4. Clean up any existing `.db` files: `rm -f *.db`

### Continuous Integration

The test suite is designed to run in CI/CD pipelines:
- All tests are isolated and can run in parallel
- No external dependencies required
- Clear pass/fail reporting

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
