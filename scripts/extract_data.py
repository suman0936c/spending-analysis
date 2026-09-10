"""Create the SQL and web-app CSV from the original workbook's data sheet."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "expense.xlsx"
TARGET = ROOT / "data" / "expense_data.csv"
RENAME_MAP = {
    "DATE": "expense_date", "DAY": "day_name", "DAY_TYPE": "day_type",
    "CATEGORY": "category", "DESCRIPTION": "description", "AMOUNT": "amount",
    "PAYMENT_MODE": "payment_mode",
}


def main() -> None:
    data = pd.read_excel(SOURCE, sheet_name="data", usecols=list(RENAME_MAP))
    data = data.rename(columns=RENAME_MAP)
    data["expense_date"] = pd.to_datetime(data["expense_date"]).dt.date
    data["amount"] = pd.to_numeric(data["amount"])
    data.to_csv(TARGET, index=False)
    print(f"Wrote {len(data)} transactions to {TARGET}")


if __name__ == "__main__":
    main()
