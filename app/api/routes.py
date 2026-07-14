"""API routes for FinancePilot.

This module defines the HTTP endpoints used by the FastAPI app. We keep
route implementations thin by delegating parsing and persistence to the
`app.services.transaction` helpers.
"""
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.transaction import parse_monefy_csv, save_transactions
from app.database.models import Transaction
from app.schemas.transaction import TransactionOut, UploadResponse

router = APIRouter()


@router.post("/upload", summary="Upload Monefy CSV", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
	"""Accept a CSV upload, parse it, and persist transactions.

	Key points:
	- We validate the filename ends with `.csv` as a basic check.
	- `UploadFile` provides an async interface; we read the bytes and pass
	  them to the parsing helper to keep I/O and parsing concerns separate.
	- Errors during parsing or if no records are found are translated into
	  HTTP 400 responses with helpful messages.
	- The endpoint returns the number of created records on success.
	"""
	if not file.filename.lower().endswith(".csv"):
		raise HTTPException(status_code=400, detail="Only CSV files are supported.")
	content = await file.read()
	try:
		records = parse_monefy_csv(content)
	except Exception as exc:
		# Return a clear client error instead of letting an internal
		# exception propagate as a 500. In production we might log details
		# and return a more generic message.
		raise HTTPException(status_code=400, detail=f"CSV parsing failed: {exc}")
	if not records:
		raise HTTPException(status_code=400, detail="No transactions found in CSV.")
	total = save_transactions(db, records)
	return {"status": "success", "created": total}


@router.get("/transactions", summary="List transactions", response_model=List[TransactionOut])
def list_transactions(
	db: Session = Depends(get_db),
	skip: int = Query(0, ge=0, description="Number of rows to skip"),
	limit: int = Query(50, ge=1, le=200, description="Maximum number of rows to return"),
):
	"""Return transactions in pages so Swagger and clients load quickly.

	The endpoint defaults to returning the newest 50 transactions. You can
	use `skip` and `limit` to request later pages.
	"""
	results = db.query(Transaction).order_by(Transaction.id.desc()).offset(skip).limit(limit).all()
	return results
