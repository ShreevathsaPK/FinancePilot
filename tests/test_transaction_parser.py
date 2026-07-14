from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, Transaction
from app.services.transaction import parse_monefy_csv, save_transactions


def test_parse_monefy_csv_with_sample_file():
    csv_path = Path("uploads/Monefy.Data.6-2-26.csv")
    with csv_path.open("rb") as handle:
        rows = parse_monefy_csv(handle.read())

    assert len(rows) > 0
    first = rows[0]
    assert first["date"] == "30/12/2020"
    assert first["description"] == "Bhel puri"
    assert first["category"] == "Eating out"
    assert first["amount"] == -15.0
    assert first["currency"] == "INR"


def test_parse_monefy_csv_with_commas_in_amount():
    sample_csv = b'date,description,category,amount,currency\n01/01/2021,Rent,House,"-12,500",INR\n'

    rows = parse_monefy_csv(sample_csv)

    assert len(rows) == 1
    assert rows[0]["amount"] == -12500.0


def test_parse_monefy_csv_header_case_insensitive_and_default_currency():
    sample_csv = b'Date,Description,Category,Amount,Currency\n01/02/2021,Taxi,Transport,100.00,\n'

    rows = parse_monefy_csv(sample_csv)

    assert len(rows) == 1
    row = rows[0]
    assert row["date"] == "01/02/2021"
    assert row["description"] == "Taxi"
    assert row["category"] == "Transport"
    assert row["amount"] == 100.0
    assert row["currency"] == "INR"


def test_parse_monefy_csv_with_empty_input_returns_empty_list():
    rows = parse_monefy_csv(b"")

    assert rows == []


def test_save_transactions_creates_records_in_database():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    records = [
        {
            "date": "10/10/2021",
            "description": "Coffee",
            "category": "Food",
            "amount": 4.5,
            "currency": "INR",
        }
    ]

    created = save_transactions(db, records)

    assert created == 1
    assert db.query(Transaction).count() == 1

    saved = db.query(Transaction).first()
    assert saved.description == "Coffee"
    assert saved.amount == 4.5
    assert saved.currency == "INR"

    db.close()
