"""
V0.3.1 Database Validation
Speedway Manager 1976

Validates the three historical 1976 databases and their
cross-database relationships.

This script is READ-ONLY. It does not modify any database.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Set


# ----------------------------------------------------------------------
# PROJECT PATH
# ----------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "database"


# ----------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------

from core.databases.rider_database_manager import (
    RiderDatabaseManager,
)

from core.databases.club_database_manager import (
    ClubDatabaseManager,
)

from core.databases.fixture_database_manager import (
    FixtureDatabaseManager,
)


# ----------------------------------------------------------------------
# VALIDATION RESULT
# ----------------------------------------------------------------------


class ValidationResult:
    """Stores validation errors and warnings."""

    def __init__(self) -> None:

        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------


def normalise_name(value: str) -> str:
    """Normalise a team or club name for comparison."""

    return " ".join(
        str(value).strip().lower().split()
    )


def print_header(title: str) -> None:
    """Print a formatted validation section header."""

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_result(
    label: str,
    passed: bool,
) -> None:
    """Print a PASS or FAIL result."""

    status = "PASS" if passed else "FAIL"

    print(
        f"[{status}] {label}"
    )


# ----------------------------------------------------------------------
# LOAD DATABASES
# ----------------------------------------------------------------------


def load_databases(result: ValidationResult):
    """Load all three historical databases."""

    print_header(
        "V0.3.1 — LOAD HISTORICAL DATABASES"
    )

    rider_path = (
        DATABASE_DIR / "riders_1976.json"
    )

    club_path = (
        DATABASE_DIR / "clubs_1976.json"
    )

    fixture_path = (
        DATABASE_DIR / "fixtures_1976.json"
    )

    riders = None
    clubs = None

        validate_clubs(
            clubs,
            result,
        )

    if fixtures is not None:

        validate_fixtures(
            fixtures,
            result,
        )

    # --------------------------------------------------------------
    # Cross-reference validation
    # --------------------------------------------------------------

    if (
        riders is not None
        and clubs is not None
    ):

        validate_rider_club_links(
            riders,
            clubs,
            result,
        )

    if (
        fixtures is not None
        and clubs is not None
    ):

        validate_fixture_club_links(
            fixtures,
            clubs,
            result,
        )

    # --------------------------------------------------------------
    # Date validation
    # --------------------------------------------------------------

    if fixtures is not None:

        validate_1976_dates(
            fixtures,
            result,
        )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    print_summary(
        result
    )

    return result.passed


# ----------------------------------------------------------------------
# SCRIPT ENTRY POINT
# ----------------------------------------------------------------------


if __name__ == "__main__":

    success = run_validation()

    sys.exit(
        0 if success else 1
    )
```
