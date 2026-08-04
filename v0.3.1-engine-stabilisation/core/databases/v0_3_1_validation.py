```python
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
    fixtures = None

    # --------------------------------------------------------------
    # RIDERS
    # --------------------------------------------------------------

    try:

        rider_manager = RiderDatabaseManager(
            rider_path
        )

        riders = rider_manager.load_database()

        print_result(
            f"Riders loaded: {len(riders)}",
            True,
        )

    except Exception as exc:

        result.error(
            f"Rider database failed to load: {exc}"
        )

        print_result(
            "Rider database",
            False,
        )

    # --------------------------------------------------------------
    # CLUBS
    # --------------------------------------------------------------

    try:

        club_manager = ClubDatabaseManager(
            club_path
        )

        clubs = club_manager.load_database()

        print_result(
            f"Clubs loaded: {len(clubs)}",
            True,
        )

    except Exception as exc:

        result.error(
            f"Club database failed to load: {exc}"
        )

        print_result(
            "Club database",
            False,
        )

    # --------------------------------------------------------------
    # FIXTURES
    # --------------------------------------------------------------

    try:

        fixture_manager = FixtureDatabaseManager(
            fixture_path
        )

        fixtures = fixture_manager.load_database()

        print_result(
            f"Fixtures loaded: {len(fixtures)}",
            True,
        )

    except Exception as exc:

        result.error(
            f"Fixture database failed to load: {exc}"
        )

        print_result(
            "Fixture database",
            False,
        )

    return (
        riders,
        clubs,
        fixtures,
    )


# ----------------------------------------------------------------------
# RIDER VALIDATION
# ----------------------------------------------------------------------


def validate_riders(
    riders,
    result: ValidationResult,
) -> None:
    """Validate the loaded riders."""

    print_header(
        "RIDER DATABASE VALIDATION"
    )

    if not riders:
        result.error(
            "No riders were loaded."
        )
        return

    rider_ids: Set[str] = set()

    for rider in riders.values():

        # ----------------------------------------------------------
        # Rider ID
        # ----------------------------------------------------------

        rider_id = str(
            rider.rider_id
        ).strip()

        if not rider_id:

            result.error(
                "Rider found without a Rider ID."
            )

        elif rider_id in rider_ids:

            result.error(
                f"Duplicate Rider ID: {rider_id}"
            )

        else:

            rider_ids.add(rider_id)

        # ----------------------------------------------------------
        # Name
        # ----------------------------------------------------------

        if not rider.name.strip():

            result.error(
                f"Rider {rider_id} has no name."
            )

        # ----------------------------------------------------------
        # Team
        # ----------------------------------------------------------

        if not rider.club.strip():

            result.error(
                f"Rider {rider.name} has no Team."
            )

        # ----------------------------------------------------------
        # Age
        # ----------------------------------------------------------

        if rider.age <= 0:

            result.error(
                f"{rider.name}: invalid age "
                f"{rider.age}"
            )

        # ----------------------------------------------------------
        # CMA
        # ----------------------------------------------------------

        if rider.cma < 0:

            result.error(
                f"{rider.name}: invalid CMA "
                f"{rider.cma}"
            )

        # ----------------------------------------------------------
        # Performance attributes
        # ----------------------------------------------------------

        attributes = {
            "Gating": rider.gating,
            "Cornering": rider.cornering,
            "Passing": rider.passing,
            "Consistency": rider.consistency,
            "Fitness": rider.fitness,
            "Potential": rider.potential,
        }

        for attribute_name, value in attributes.items():

            if value < 0:

                result.error(
                    f"{rider.name}: invalid "
                    f"{attribute_name} {value}"
                )

    print_result(
        f"Rider records validated: {len(riders)}",
        True,
    )


# ----------------------------------------------------------------------
# CLUB VALIDATION
# ----------------------------------------------------------------------


def validate_clubs(
    clubs,
    result: ValidationResult,
) -> None:
    """Validate the loaded clubs."""

    print_header(
        "CLUB DATABASE VALIDATION"
    )

    if not clubs:

        result.error(
            "No clubs were loaded."
        )

        return

    club_ids: Set[str] = set()

    for club in clubs.values():

        club_id = str(
            club.club_id
        ).strip()

        # ----------------------------------------------------------
        # Club ID
        # ----------------------------------------------------------

        if not club_id:

            result.error(
                "Club found without a Club ID."
            )

        elif club_id in club_ids:

            result.error(
                f"Duplicate Club ID: {club_id}"
            )

        else:

            club_ids.add(club_id)

        # ----------------------------------------------------------
        # Club name
        # ----------------------------------------------------------

        if not club.name.strip():

            result.error(
                f"Club {club_id} has no name."
            )

        # ----------------------------------------------------------
        # Stadium
        # ----------------------------------------------------------

        if not club.stadium.strip():

            result.error(
                f"{club.name} has no stadium."
            )

        # ----------------------------------------------------------
        # Capacity
        # ----------------------------------------------------------

        if club.stadium_capacity <= 0:

            result.error(
                f"{club.name}: invalid stadium "
                f"capacity {club.stadium_capacity}"
            )

        # ----------------------------------------------------------
        # Attendance
        # ----------------------------------------------------------

        if club.average_attendance < 0:

            result.error(
                f"{club.name}: invalid average "
                f"attendance {club.average_attendance}"
            )

        # ----------------------------------------------------------
        # Track
        # ----------------------------------------------------------

        if club.track_size <= 0:

            result.error(
                f"{club.name}: invalid track size "
                f"{club.track_size}"
            )

    print_result(
        f"Club records validated: {len(clubs)}",
        True,
    )


# ----------------------------------------------------------------------
# FIXTURE VALIDATION
# ----------------------------------------------------------------------


def validate_fixtures(
    fixtures,
    result: ValidationResult,
) -> None:
    """Validate the loaded fixtures."""

    print_header(
        "FIXTURE DATABASE VALIDATION"
    )

    if not fixtures:

        result.error(
            "No fixtures were loaded."
        )

        return

    fixture_ids: Set[str] = set()

    for fixture in fixtures.values():

        fixture_id = str(
            fixture.fixture_id
        ).strip()

        # ----------------------------------------------------------
        # Fixture ID
        # ----------------------------------------------------------

        if not fixture_id:

            result.error(
                "Fixture found without an ID."
            )

        elif fixture_id in fixture_ids:

            result.error(
                f"Duplicate Fixture ID: {fixture_id}"
            )

        else:

            fixture_ids.add(fixture_id)

        # ----------------------------------------------------------
        # Teams
        # ----------------------------------------------------------

        if not fixture.home_team.strip():

            result.error(
                f"{fixture_id}: no Home Team."
            )

        if not fixture.away_team.strip():

            result.error(
                f"{fixture_id}: no Away Team."
            )

        # ----------------------------------------------------------
        # Home vs Away
        # ----------------------------------------------------------

        if (
            normalise_name(
                fixture.home_team
            )
            ==
            normalise_name(
                fixture.away_team
            )
        ):

            result.error(
                f"{fixture_id}: Home Team and "
                f"Away Team are identical: "
                f"{fixture.home_team}"
            )

        # ----------------------------------------------------------
        # Date
        # ----------------------------------------------------------

        if fixture.meeting_date is None:

            result.error(
                f"{fixture_id}: missing Meeting Date."
            )

        # ----------------------------------------------------------
        # Competition
        # ----------------------------------------------------------

        if not fixture.meeting_type.strip():

            result.error(
                f"{fixture_id}: missing Meeting Type."
            )

    print_result(
        f"Fixture records validated: {len(fixtures)}",
        True,
    )


# ----------------------------------------------------------------------
# RIDER → CLUB CROSS REFERENCE
# ----------------------------------------------------------------------


def validate_rider_club_links(
    riders,
    clubs,
    result: ValidationResult,
) -> None:
    """Check every rider's Team against the club database."""

    print_header(
        "RIDER → CLUB CROSS-REFERENCE"
    )

    club_names: Dict[str, str] = {}

    for club in clubs.values():

        club_names[
            normalise_name(club.name)
        ] = club.name

    unmatched: List[str] = []

    for rider in riders.values():

        rider_team = normalise_name(
            rider.club
        )

        if rider_team not in club_names:

            unmatched.append(
                f"{rider.name} → {rider.club}"
            )

    if unmatched:

        result.error(
            "Riders with teams not found in "
            "the club database:"
        )

        for item in unmatched:

            result.error(
                f"  {item}"
            )

        print_result(
            f"Rider → Club links "
            f"({len(unmatched)} unmatched)",
            False,
        )

    else:

        print_result(
            f"All {len(riders)} riders match "
            f"a club",
            True,
        )


# ----------------------------------------------------------------------
# FIXTURE → CLUB CROSS REFERENCE
# ----------------------------------------------------------------------


def validate_fixture_club_links(
    fixtures,
    clubs,
    result: ValidationResult,
) -> None:
    """Check fixture teams against the club database."""

    print_header(
        "FIXTURE → CLUB CROSS-REFERENCE"
    )

    club_names: Dict[str, str] = {}

    for club in clubs.values():

        club_names[
            normalise_name(club.name)
        ] = club.name

    unmatched: List[str] = []

    for fixture in fixtures.values():

        home = normalise_name(
            fixture.home_team
        )

        away = normalise_name(
            fixture.away_team
        )

        if home not in club_names:

            unmatched.append(
                f"{fixture.fixture_id}: "
                f"Home Team '{fixture.home_team}'"
            )

        if away not in club_names:

            unmatched.append(
                f"{fixture.fixture_id}: "
                f"Away Team '{fixture.away_team}'"
            )

    if unmatched:

        result.error(
            "Fixtures contain teams that do not "
            "match a club:"
        )

        for item in unmatched:

            result.error(
                f"  {item}"
            )

        print_result(
            f"Fixture → Club links "
            f"({len(unmatched)} unmatched)",
            False,
        )

    else:

        print_result(
            f"All fixture teams match "
            f"a club",
            True,
        )


# ----------------------------------------------------------------------
# SEASON DATE VALIDATION
# ----------------------------------------------------------------------


def validate_1976_dates(
    fixtures,
    result: ValidationResult,
) -> None:
    """Check that fixtures fall within the 1976 season."""

    print_header(
        "1976 SEASON DATE VALIDATION"
    )

    invalid_dates = []

    for fixture in fixtures.values():

        if fixture.meeting_date.year != 1976:

            invalid_dates.append(
                f"{fixture.fixture_id}: "
                f"{fixture.meeting_date}"
            )

    if invalid_dates:

        for item in invalid_dates:

            result.error(
                f"Fixture outside 1976: {item}"
            )

        print_result(
            f"1976 date validation "
            f"({len(invalid_dates)} errors)",
            False,
        )

    else:

        print_result(
            f"All {len(fixtures)} fixtures "
            f"are dated in 1976",
            True,
        )


# ----------------------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------------------


def print_summary(
    result: ValidationResult,
) -> None:
    """Print the final validation summary."""

    print_header(
        "V0.3.1 VALIDATION SUMMARY"
    )

    print(
        f"Errors:   {len(result.errors)}"
    )

    print(
        f"Warnings: {len(result.warnings)}"
    )

    if result.errors:

        print()
        print("ERRORS")
        print("-" * 70)

        for error in result.errors:

            print(
                f"ERROR: {error}"
            )

    if result.warnings:

        print()
        print("WARNINGS")
        print("-" * 70)

        for warning in result.warnings:

            print(
                f"WARNING: {warning}"
            )

    print()

    if result.passed:

        print(
            "RESULT: PASS"
        )

        print(
            "The three historical databases "
            "passed V0.3.1 validation."
        )

    else:

        print(
            "RESULT: FAIL"
        )

        print(
            "The 1976 world is NOT ready for "
            "WorldBuilder yet."
        )


# ----------------------------------------------------------------------
# MAIN VALIDATION
# ----------------------------------------------------------------------


def run_validation() -> bool:
    """Run the complete V0.3.1 validation."""

    result = ValidationResult()

    print()
    print("=" * 70)
    print(
        "SPEEDWAY MANAGER 1976"
    )
    print(
        "VERSION 0.3.1 DATABASE VALIDATION"
    )
    print("=" * 70)

    print()
    print(
        f"Database directory:"
        f" {DATABASE_DIR}"
    )

    # --------------------------------------------------------------
    # LOAD
    # --------------------------------------------------------------

    riders, clubs, fixtures = load_databases(
        result
    )

    # --------------------------------------------------------------
    # Individual validation
    # --------------------------------------------------------------

    if riders is not None:

        validate_riders(
            riders,
            result,
        )

    if clubs is not None:

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
