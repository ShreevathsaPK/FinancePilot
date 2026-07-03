"""
Database connection utilities.

This module sets up the SQLAlchemy `engine` and a `SessionLocal` factory.
FastAPI endpoints can depend on `get_db()` to receive a database session
which is automatically closed after the request completes.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

# Create an engine. `future=True` enables SQLAlchemy 2.0 style usage while
# remaining compatible with the code in this project.
engine = create_engine(DATABASE_URL, echo=False, future=True)

# SessionLocal is a factory for new Session objects. We configure it with
# `autoflush=False` and `autocommit=False` for explicit transaction control.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
	"""Yield a database session and ensure it is closed afterwards.

	Use this function as a dependency in FastAPI endpoints. Example:

		def endpoint(db: Session = Depends(get_db)):
			...

	The `yield` pattern ensures the session is closed even if errors occur.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
