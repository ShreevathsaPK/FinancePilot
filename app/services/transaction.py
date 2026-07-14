"""
Transaction parsing and persistence helpers.

This module contains two main responsibilities:
1. Parse a Monefy-exported CSV into a list of Python dictionaries.
2. Persist those dictionaries into the database using SQLAlchemy sessions.

Splitting parsing and persistence keeps the code easier to test.
"""
import csv
from io import StringIO
from typing import List

from sqlalchemy.orm import Session

from app.database.models import Transaction


def parse_monefy_csv(file_bytes: bytes) -> List[dict]:
	"""Parse a CSV file produced by Monefy (or similar) into a list of
	plain dictionaries.

	Expectations and behavior:
	- `file_bytes` should be the raw bytes from an uploaded CSV file.
	- We decode using UTF-8 and use `errors='replace'` to avoid failures on
	  unexpected characters; for production you may want stricter validation.
	- We use `csv.DictReader` so fields are accessed by header name. Common
	  headers include `date`, `description`, `category`, `amount`, `currency`.
	- Amounts may include commas (e.g. `-12,500`), so we remove commas
	  before converting to float.
	- The function returns a list of dicts with the keys: `date`,
	  `description`, `category`, `amount`, `currency`.
	"""
	content = file_bytes.decode("utf-8", errors="replace")
	reader = csv.DictReader(StringIO(content))
	transactions = []
	for row in reader:
		# Normalize header names to lowercase, so `Date` and `date` both work.
		normalized = {key.strip().lower(): value for key, value in row.items() if key}
		amount_raw = normalized.get("amount", "0")
		amount = 0.0
		if amount_raw:
			# Normalize quoted or comma-formatted amounts like "-12,500".
			amount_text = str(amount_raw).strip().replace("\"", "")
			amount = float(amount_text.replace(",", ""))

		transactions.append(
			{
				"date": normalized.get("date", "").strip(),
				"description": normalized.get("description", "").strip(),
				"category": normalized.get("category", "").strip(),
				"amount": amount,
				"currency": normalized.get("currency", "INR").strip() or "INR",
			}
		)
	return transactions


def save_transactions(db: Session, records: List[dict]) -> int:
	"""Persist parsed records into the database using an active SQLAlchemy
	`Session`.

	Important notes:
	- This function expects the caller to provide a `Session` instance
	  (for example via FastAPI's dependency injection with `get_db`).
	- We add objects to the session and call `commit()` once at the end for
	  efficiency. In larger imports you might want to batch commits and
	  handle rollback on errors.
	- Returns the number of records created.
	"""
	created = 0
	for record in records:
		tx = Transaction(
			date=record["date"],
			description=record["description"],
			category=record.get("category"),
			amount=record["amount"],
			currency=record.get("currency", "INR"),
		)
		db.add(tx)
		created += 1
	db.commit()
	return created
