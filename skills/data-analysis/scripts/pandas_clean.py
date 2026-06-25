"""
Safe snippet for basic pandas cleaning. Copy and adapt for your dataset.
Run: python pandas_clean.py  (ensure pandas is installed)
"""
import sys
from pathlib import Path

import pandas as pd


DEBUG_MODE = "--debug" in sys.argv


def debug_print(*args, **kwargs) -> None:
	if DEBUG_MODE:
		print(*args, **kwargs)

def main() -> int:
	data_path = Path("data.csv")

	if not data_path.exists():
		print(f"ERROR: Input file not found: {data_path}", file=sys.stderr)
		return 1

	try:
		# Load (adjust path and kwargs as needed)
		df = pd.read_csv(data_path)  # or read_json, read_excel
	except (FileNotFoundError, PermissionError, pd.errors.ParserError, OSError) as exc:
		print(f"ERROR: Failed to load CSV file: {exc}", file=sys.stderr)
		return 1

	if df.empty:
		print("ERROR: Input dataset is empty. Nothing to process.", file=sys.stderr)
		return 1

	debug_print("df_shape", df.shape)
	debug_print("df_dtypes", df.dtypes)

	try:
		# Drop fully null columns
		df = df.dropna(axis=1, how="all")
		debug_print("df_shape_after_drop_all_null_cols", df.shape)

		# Fill or drop nulls in key columns (customise columns)
		# df = df.dropna(subset=["required_col"])
		# df["optional_col"] = df["optional_col"].fillna(0)

		# Normalise column names (optional)
		df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
		debug_print("df_columns", list(df.columns))

		# Deduplicate (optional)
		before = len(df)
		df = df.drop_duplicates()
		debug_print("rows_dropped_duplicates", before - len(df))

		# Sample output
		debug_print("df_head", df.head())
	except Exception as exc:
		print(f"ERROR: Data processing failed: {exc}", file=sys.stderr)
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())
