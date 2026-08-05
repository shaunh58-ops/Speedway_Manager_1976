"""
V0.3.1 Database Validation
Speedway Manager 1976

Validates the three historical 1976 databases and their
cross-database relationships.

This script is READ-ONLY. It does not modify any database.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path


# ----------------------------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "database"


# ----------------------------------------------------------------------
# DATABASE MANAGERS
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
        self.errors = []
        self.warnings = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


# ----------------------------------------------------------------------
# DISPLAY HELPERS
# ----------------------------------------------------------------------


def print_header(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_result(
    label: str,
    passed: bool,
) -> None:

    status = "PASS" if passed else "FAIL"

    print(
        f"[{status}] {label}"
    )


# ----------------------------------------------------------------------
# NAME NORMALISATION
# ----------------------------------------------------------------------


def normalise_name(value: str) -> str:

    return " ".join(
        str(value).strip().lower().split()
    )


# ----------------------------------------------------------------------
# LOAD DATABASES
# ----------------------------------------------------------------------


def load_databases(result: ValidationResult):

    print_header(
        "V0.3.1 - LOAD HISTORICAL DATABASES"
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

    riders = {}
    clubs = {}
    fixtures = {}

    # --------------------------------------------------------------
    # Riders
    # --------------------------------------------------------------

    try:

        manager = RiderDatabaseManager()

        riders = manager.load_database(
            rider_path
        )

        print_result(
            f"Riders loaded: {len(riders)}",
            len(riders) == 152,
        )

        if len(riders) != 152:
            result.warning(
                f"Expected 152 riders but found {len(riders)}"
            )

    except Exception as exc:

        result.error(
            f"Rider database failed to load: {exc}"
        )

        print_result(
            "Rider database load",
            False,
        )

    # --------------------------------------------------------------
    # Clubs
    # --------------------------------------------------------------

    try:

        manager = ClubDatabaseManager()

        clubs = manager.load_database(
            club_path
        )

        print_result(
            f"Clubs loaded: {len(clubs)}",
            len(clubs) == 19,
        )

        if len(clubs) != 19:
            result.warning(
                f"Expected 19 clubs but found {len(clubs)}"
            )

    except Exception as exc:

        result.error(
            f"Club database failed to load: {exc}"
        )

        print_result(
            "Club database load",
            False,
        )

    # --------------------------------------------------------------
    # Fixtures
    # --------------------------------------------------------------

    try:

        manager = FixtureDatabaseManager()

        fixtures = manager.load_database(
            fixture_path
        )

        print_result(
            f"Fixtures loaded: {len(fixtures)}",
            len(fixtures) == 342,
        )

        if len(fixtures) != 342:
            result.warning(
                f"Expected 342 fixtures but found {len(fixtures)}"
            )

    except Exception as exc:

        result.error(
            f"Fixture database failed to load: {exc}"
        )

        print_result(
            "Fixture database load",
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

    print_header(
        "RIDER DATABASE VALIDATION"
    )

    if not riders:

        result.error(
            "Rider database is empty"
        )

        print_result(
            "Rider database contains records",
            False,
        )

        return

    required_fields = (
        "rider_id",
        "name",
        "club",
        "age",
        "nationality",
        "cma",
    )

    valid = True

    for rider_id, rider in riders.items():

        for field in required_fields:

            if not hasattr(
                rider,
                field
            ):

                result.error(
                    f"Rider {rider_id} missing field: {field}"
                )

                valid = False

    print_result(
        "Rider required fields",
        valid,
    )


# ----------------------------------------------------------------------
# CLUB VALIDATION
# ----------------------------------------------------------------------


def validate_clubs(
    clubs,
    result: ValidationResult,
) -> None:

    print_header(
        "CLUB DATABASE VALIDATION"
    )

    if not clubs:

        result.error(
            "Club database is empty"
        )

        print_result(
            "Club database contains records",
            False,
        )

        return

    required_fields = (
        "club_id",
        "name",
        "stadium",
        "stadium_capacity",
        "average_attendance",
        "track_size",
        "race_night",
    )

    valid = True

    for club_id, club in clubs.items():

        for field in required_fields:

            if not hasattr(
                club,
                field
            ):

                result.error(
                    f"Club {club_id} missing field: {field}"
                )

                valid = False

    print_result(
        "Club required fields",
        valid,
    )


# ----------------------------------------------------------------------
# FIXTURE VALIDATION
# ----------------------------------------------------------------------


def validate_fixtures(
    fixtures,
    result: ValidationResult,
) -> None:

    print_header(
        "FIXTURE DATABASE VALIDATION"
    )

    if not fixtures:

        result.error(
            "Fixture database is empty"
        )

        print_result(
            "Fixture database contains records",
            False,
        )

        return

    required_fields = (
        "fixture_id",
        "meeting_date",
        "home_team",
        "away_team",
        "meeting_type",
    )

    valid = True

    for fixture_id, fixture in fixtures.items():

        for field in required_fields:

            if not hasattr(
                fixture,
                field
            ):

                result.error(
                    f"Fixture {fixture_id} missing field: {field}"
                )

                valid = False

    print_result(
        "Fixture required fields",
        valid,
    )


# ----------------------------------------------------------------------
# RIDER / CLUB CROSS REFERENCES
# ----------------------------------------------------------------------


def validate_rider_club_links(
    riders,
    clubs,
    result: ValidationResult,
) -> None:

    print_header(
        "RIDER -> CLUB CROSS-REFERENCE"
    )

    club_names = {
        normalise_name(
            club.name
        )
        for club in clubs.values()
    }

    invalid = []

    for rider in riders.values():

        rider_club = normalise_name(
            rider.club
        )

        if rider_club not in club_names:

            invalid.append(
                f"{rider.name} -> {rider.club}"
            )

    if invalid:

        result.error(
            f"{len(invalid)} rider club references are invalid"
        )

        for item in invalid[:10]:

            print(
                f"  INVALID: {item}"
            )

        print_result(
            "All rider club references",
            False,
        )

    else:

        print_result(
            "All rider club references",
            True,
        )


# ----------------------------------------------------------------------
# FIXTURE / CLUB CROSS REFERENCES
# ----------------------------------------------------------------------


def validate_fixture_club_links(
    fixtures,
    clubs,
    result: ValidationResult,
) -> None:

    print_header(
        "FIXTURE -> CLUB CROSS-REFERENCE"
    )

    club_names = {
        normalise_name(
            club.name
        )
        for club in clubs.values()
    }

    invalid = []

    for fixture in fixtures.values():

        home = normalise_name(
            fixture.home_team
        )

        away = normalise_name(
            fixture.away_team
        )

        if home not in club_names:

            invalid.append(
                f"{fixture.fixture_id}: HOME {fixture.home_team}"
            )

        if away not in club_names:

            invalid.append(
                f"{fixture.fixture_id}: AWAY {fixture.away_team}"
            )

    if invalid:

        result.error(
            f"{len(invalid)} fixture club references are invalid"
        )

        for item in invalid[:10]:

            print(
                f"  INVALID: {item}"
            )

        print_result(
            "All fixture club references",
            False,
        )

    else:

        print_result(
            "All fixture club references",
            True,
        )


# ----------------------------------------------------------------------
# DATE VALIDATION
# ----------------------------------------------------------------------


def validate_1976_dates(
    fixtures,
    result: ValidationResult,
) -> None:

    print_header(
        "1976 DATE VALIDATION"
    )

    invalid = []

    for fixture in fixtures.values():

        try:

            date = datetime.strptime(
                fixture.meeting_date,
                "%d/%m/%Y",
            )

            if date.year != 1976:

                invalid.append(
                    f"{fixture.fixture_id}: "
                    f"{fixture.meeting_date}"
                )

        except ValueError:

            invalid.append(
                f"{fixture.fixture_id}: "
                f"{fixture.meeting_date}"
            )

    if invalid:

        result.error(
            f"{len(invalid)} fixture dates are invalid"
        )

        for item in invalid[:10]:

            print(
                f"  INVALID: {item}"
            )

        print_result(
            "All fixture dates are valid 1976 dates",
            False,
        )

    else:

        print_result(
            "All fixture dates are valid 1976 dates",
            True,
        )


# ----------------------------------------------------------------------
# DUPLICATE VALIDATION
# ----------------------------------------------------------------------


def validate_unique_ids(
    riders,
    clubs,
    fixtures,
    result: ValidationResult,
) -> None:

    print_header(
        "ID VALIDATION"
    )

    rider_ids = list(
        riders.keys()
    )

    club_ids = list(
        clubs.keys()
    )

    fixture_ids = list(
        fixtures.keys()
    )

    rider_unique = (
        len(rider_ids)
        == len(set(rider_ids))
    )

    club_unique = (
        len(club_ids)
        == len(set(club_ids))
    )

    fixture_unique = (
        len(fixture_ids)
        == len(set(fixture_ids))
    )

    print_result(
        "Rider IDs unique",
        rider_unique,
    )

    print_result(
        "Club IDs unique",
        club_unique,
    )

    print_result(
        "Fixture IDs unique",
        fixture_unique,
    )

    if not rider_unique:
        result.error(
            "Duplicate rider IDs detected"
        )

    if not club_unique:
        result.error(
            "Duplicate club IDs detected"
        )

    if not fixture_unique:
        result.error(
            "Duplicate fixture IDs detected"
        )


# ----------------------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------------------


def print_summary(
    result: ValidationResult
) -> None:

    print_header(
        "V0.3.1 VALIDATION SUMMARY"
    )

    print(
        f"Errors: {len(result.errors)}"
    )

    print(
        f"Warnings: {len(result.warnings)}"
    )

    if result.errors:

        print()

        print(
            "ERRORS:"
        )

        for error in result.errors:

            print(
                f"  - {error}"
            )

    if result.warnings:

        print()

        print(
            "WARNINGS:"
        )

        for warning in result.warnings:

            print(
                f"  - {warning}"
            )

    print()

    if result.passed:

        print(
            "V0.3.1 VALIDATION: PASS"
        )

    else:

        print(
            "V0.3.1 VALIDATION: FAIL"
        )


# ----------------------------------------------------------------------
# MAIN VALIDATION
# ----------------------------------------------------------------------


def run_validation() -> bool:

    result = ValidationResult()

    (
        riders,
        clubs,
        fixtures,
    ) = load_databases(
        result
    )

    if riders:

        validate_riders(
            riders,
            result,
        )

    if clubs:

        validate_clubs(
            clubs,
            result,
        )

    if fixtures:

        validate_fixtures(
            fixtures,
            result,
        )

    if riders and clubs:

        validate_rider_club_links(
            riders,
            clubs,
            result,
        )

    if fixtures and clubs:

        validate_fixture_club_links(
            fixtures,
            clubs,
            result,
        )

    if fixtures:

        validate_1976_dates(
            fixtures,
            result,
        )

    validate_unique_ids(
        riders,
        clubs,
        fixtures,
        result,
    )

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