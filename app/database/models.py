"""
Database models for FinancePilot.

This module defines SQLAlchemy ORM models used to persist transaction
records. Each model maps to a database table and declares column types
and constraints.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.orm import declarative_base

# Base class for ORM models. `declarative_base()` produces a base that
# SQLAlchemy uses to keep track of mapped classes and tables.
Base = declarative_base()


class Transaction(Base):
	"""A simple transaction record representing one CSV row.

	Fields:
	- `id`: integer primary key
	- `date`: original date string from the CSV (kept as string for now)
	- `description`: transaction description
	- `category`: optional user-assigned category
	- `amount`: numeric value (positive for income, negative for expense)
	- `currency`: currency code (default 'INR')
	- `created_at`: timestamp when the row was inserted

	Note: For a production system you may want to normalize dates to
	`Date`/`DateTime` types and add indexes for commonly queried fields.
	"""
	__tablename__ = "transactions"

	id = Column(Integer, primary_key=True, index=True)
	date = Column(String, nullable=False)
	description = Column(String, nullable=False)
	category = Column(String, nullable=True)
	amount = Column(Float, nullable=False)
	currency = Column(String, nullable=True, default="INR")
	created_at = Column(DateTime, default=datetime.utcnow)
