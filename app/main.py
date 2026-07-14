"""
Application entrypoint for FastAPI.

This module creates the FastAPI app, includes the API router and ensures the
database tables are created on startup. Keeping the app object in
`app.main:app` makes it easy to run with `uvicorn`.
"""
from fastapi import FastAPI

from app.api.routes import router as api_router
from app.config import APP_TITLE, APP_VERSION
from app.database.connection import engine
from app.database.models import Base


app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Mount the API router under /api so all endpoints are namespaced.
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def on_startup():
	"""Create database tables on startup if they do not exist.

	This ensures a local development environment is ready to receive data
	without a separate migration step. For production you should use proper
	migrations (for example Alembic) instead of calling `create_all`.
	"""
	Base.metadata.create_all(bind=engine)


@app.get("/", summary="Service health")
def root():
	"""A minimal health-check endpoint used to verify the service started."""
	return {"status": "ok", "service": "FinancePilot"}
