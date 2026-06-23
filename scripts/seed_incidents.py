#!/usr/bin/env python3
"""Seed incidents from a CSV file into backoffice JSON storage.

This script is idempotent by using a deterministic fingerprint per row.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {"open", "in_progress", "resolved", "discarded"}
ALLOWED_ORIGINS = {"customer", "branch", "internal"}
ALLOWED_CATEGORIES = {
    "lost_parcel",
    "failed_delivery",
    "wrong_address",
    "inventory_discrepancy",
}
ALLOWED_BRANCHES = {"Los Angeles", "Zaragoza", "Central"}

DEFAULT_INPUT_COLUMNS = [
    "title",
    "description",
    "category",
    "branch",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed incidents from CSV")
    parser.add_argument(
        "--csv-path",
        required=True,
        help="Path to input CSV with incident rows",
    )
    parser.add_argument(
        "--data-path",
        default="uis/backoffice/data/incidents.json",
        help="Path to incidents JSON store",
    )
    parser.add_argument(
        "--id-columns",
        default=",".join(DEFAULT_INPUT_COLUMNS),
        help="Comma-separated identifying columns for idempotency fingerprint",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report without writing",
    )
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_store(path: Path) -> list[dict[str, Any]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]\n", encoding="utf-8")
        return []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if not isinstance(payload, list):
        return []

    return [row for row in payload if isinstance(row, dict)]


def row_fingerprint(row: dict[str, str], id_columns: list[str]) -> str:
    basis = "|".join((row.get(key, "") or "").strip().lower() for key in id_columns)
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def validate_row(row: dict[str, str], index: int) -> list[str]:
    errors: list[str] = []

    title = (row.get("title") or "").strip()
    description = (row.get("description") or "").strip()
    category = (row.get("category") or "").strip()
    branch = (row.get("branch") or "").strip()

    if not title:
        errors.append(f"row {index}: title is required")
    if not description:
        errors.append(f"row {index}: description is required")
    if category not in ALLOWED_CATEGORIES:
        errors.append(f"row {index}: category '{category}' is not allowed")
    if branch not in ALLOWED_BRANCHES:
        errors.append(f"row {index}: branch '{branch}' is not allowed")

    return errors


def build_incident(row: dict[str, str], fingerprint: str) -> dict[str, Any]:
    timestamp = now_iso()

    # Use deterministic id so reruns remain idempotent even without DB constraints.
    incident_id = f"inc_seed_{fingerprint[:16]}"

    return {
        "id": incident_id,
        "title": (row.get("title") or "").strip(),
        "description": (row.get("description") or "").strip(),
        "category": (row.get("category") or "").strip(),
        "status": "open",
        "origin": "customer",
        "branch": (row.get("branch") or "").strip(),
        "created_at": timestamp,
        "updated_at": timestamp,
        "seed_fingerprint": fingerprint,
    }


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv_path)
    data_path = Path(args.data_path)
    id_columns = [column.strip() for column in args.id_columns.split(",") if column.strip()]

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 1

    if not id_columns:
        print("At least one id column is required for idempotency")
        return 1

    incidents = ensure_store(data_path)
    known_fingerprints = {
        str(incident.get("seed_fingerprint"))
        for incident in incidents
        if incident.get("seed_fingerprint")
    }

    inserted = 0
    skipped_duplicates = 0
    invalid_rows: list[str] = []

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            print("CSV has no header row")
            return 1

        for index, row in enumerate(reader, start=2):
            row_errors = validate_row(row, index)
            if row_errors:
                invalid_rows.extend(row_errors)
                continue

            fingerprint = row_fingerprint(row, id_columns)
            if fingerprint in known_fingerprints:
                skipped_duplicates += 1
                continue

            incidents.append(build_incident(row, fingerprint))
            known_fingerprints.add(fingerprint)
            inserted += 1

    if not args.dry_run:
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data_path.write_text(f"{json.dumps(incidents, indent=2)}\n", encoding="utf-8")

    print("Seed summary")
    print(f"- inserted: {inserted}")
    print(f"- skipped_duplicates: {skipped_duplicates}")
    print(f"- invalid_rows: {len(invalid_rows)}")

    if invalid_rows:
        print("Invalid row details:")
        for issue in invalid_rows:
            print(f"  - {issue}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
