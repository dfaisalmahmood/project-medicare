# Backend

FastAPI app with modular structure. Key modules:

- Auth: JWT login/register
- Users: Admin CRUD
- Patients: Per-user profiles and health-record identity

Run dev server:

```
uv run fastapi dev --reload --host 0.0.0.0 --port 8000
```

Seed superadmin:

```
uv run python -m app.seed_superadmin
```

# Project Medicare Backend

This project is the backend service for Project Medicare, built using FastAPI and managed with uv. It provides a robust API for managing healthcare data and integrates with a PostgreSQL database.

## Development

### Prerequisites

- astral uv
- Python 3.12+
- docker & docker-compose (for local development with PostgreSQL)

### Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Run the Docker containers:

   ```bash
   docker-compose up -d
   ```

3. Run the development server:

   ```bash
   uv run fastapi dev app/main.py --port 8000

   ```

4. Environment variables (dev defaults shown):

   - DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5451/project_medicare
   - JWT_SECRET_KEY=change-me
   - JWT_ALGORITHM=HS256
   - ACCESS_TOKEN_EXPIRE_MINUTES=60

## API

- Auth:
  - POST /api/auth/register
  - POST /api/auth/login
- Users:

  - GET /api/users/
  - GET /api/users/me (requires Bearer token)

  ```

  ```
