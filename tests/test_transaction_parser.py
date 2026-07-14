from pathlib import Path

from app.services.transaction import parse_monefy_csv


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
