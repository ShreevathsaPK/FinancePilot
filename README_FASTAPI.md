# FinancePilot — FastAPI Overview

This short guide explains the small FastAPI app in this repository and
how the pieces fit together. It is intended for beginners learning how
to build a simple CSV upload + parse + store pipeline.

Files of interest
- `app/main.py`: FastAPI application entrypoint. It creates the `app`
  object, includes the API router and creates database tables on startup.
- `app/api/routes.py`: HTTP endpoints. `/api/upload` accepts CSV uploads
  and `/api/transactions` lists stored records.
- `app/services/transaction.py`: CSV parsing logic and persistence helper
  functions.
- `app/database/connection.py`: SQLAlchemy engine and `get_db` dependency
  used by endpoints to obtain a DB session.
- `app/database/models.py`: ORM model (`Transaction`) used to store data.

Running locally

1. Activate the virtual environment if not already active:

```bash
cd /path/to/FinancePilot
.venv/bin/activate
```

2. Start the app with Uvicorn (reload for development):

```bash
.venv/bin/uvicorn app.main:app --reload
```

3. Open the interactive docs at `http://127.0.0.1:8000/docs` to try the
   upload endpoint and inspect responses.

Notes for learning
- The project keeps parsing and database logic separate: this makes code
  easier to test and reason about.
- `get_db()` is used as a FastAPI dependency so each request gets its own
  DB session which is closed automatically.
- For production you should add proper validation (Pydantic models),
  pagination for list endpoints, and database migrations (Alembic).

If you'd like, I can now:

- Add Pydantic request/response models and input validation.
- Add unit tests for the CSV parser.
- Implement pagination and filters for `/api/transactions`.
