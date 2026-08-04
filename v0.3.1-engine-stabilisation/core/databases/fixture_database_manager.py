"""
Fixture Database Manager
Speedway Manager 1976

Loads and manages the historical 1976 fixture database.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Union

from core.logger import get_logger


log = get_logger("FixtureDatabaseManager")


@dataclass
class Fixture:
    """Represents a Speedway fixture during the 1976 season."""

    fixture_id: str
    meeting_date: date
    home_team: str
    away_team: str
    meeting_type: str

    # Dynamic result data
    completed: bool = False
    home_score: int = 0
    away_score: int = 0

    @property
    def is_home_win(self) -> bool:
        """Return True if the home team won."""

        return (
            self.completed
            and self.home_score > self.away_score
        )

    @property
    def is_away_win(self) -> bool:
        """Return True if the away team won."""

        return (
            self.completed
            and self.away_score > self.home_score
        )

    @property
    def is_draw(self) -> bool:
        """Return True if the fixture was drawn."""

        return (
            self.completed
            and self.home_score == self.away_score
        )


class FixtureDatabaseManager:
    """Loads and provides access to the 1976 fixture database."""

    def __init__(
        self,
        database_path: Optional[Union[str, Path]] = None,
    ) -> None:

        self.database_path = (
            Path(database_path)
            if database_path is not None
            else None
        )

        self.fixtures: Dict[str, Fixture] = {}

    # ------------------------------------------------------------------
    # DATABASE LOADING
    # ------------------------------------------------------------------

    def load_database(
        self,
        file_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Fixture]:
        """
        Load the historical 1976 fixture database.

        The current JSON format is:

        [
            {
                "Meeting Date": "19/03/1976",
                "Home Team": "Hackney",
                "Away Team": "Newport",
                "Meeting Type": "British League"
            }
        ]
        """

        path = Path(file_path) if file_path else self.database_path

        if path is None:
            raise ValueError(
                "No fixture database path has been supplied."
            )

        if not path.exists():
            raise FileNotFoundError(
                f"Fixture database not found: {path}"
            )

        log.info("Loading fixture database: %s", path)

        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        records = self._extract_records(raw_data)

        self.fixtures.clear()

        for index, record in enumerate(
            records,
            start=1,
        ):

            try:

                fixture = self.create_fixture(
                    record,
                    index,
                )

                if fixture.fixture_id in self.fixtures:
                    raise ValueError(
                        f"Duplicate fixture ID: "
                        f"{fixture.fixture_id}"
                    )

                self.fixtures[
                    fixture.fixture_id
                ] = fixture

            except Exception as exc:

                raise ValueError(
                    f"Error loading fixture "
                    f"record {index}: {exc}"
                ) from exc

        log.info(
            "Successfully loaded %s fixtures.",
            len(self.fixtures),
        )

        return self.fixtures

    # ------------------------------------------------------------------
    # RECORD EXTRACTION
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_records(raw_data) -> List[dict]:
        """Extract fixture records from supported JSON structures."""

        if isinstance(raw_data, list):
            records = raw_data

        elif isinstance(raw_data, dict):
            records = raw_data.get("data")

        else:
            records = None

        if not isinstance(records, list):
            raise ValueError(
                "Fixture database must contain a JSON list "
                "or an object containing a 'data' list."
            )

        return records

    # ------------------------------------------------------------------
    # FIXTURE CREATION
    # ------------------------------------------------------------------

    def create_fixture(
        self,
        data: dict,
        index: int,
    ) -> Fixture:
        """Convert a JSON fixture record into a Fixture object."""

        fixture_id = self._text(
            data.get("Fixture ID")
        )

        # Fixture IDs are generated because the historical
        # JSON does not currently contain them.
        if not fixture_id:
            fixture_id = (
                f"F1976-{index:04d}"
            )

        home_team = self._text(
            data.get("Home Team")
        )

        away_team = self._text(
            data.get("Away Team")
        )

        meeting_type = self._text(
            data.get("Meeting Type")
        )

        if not home_team:
            raise ValueError(
                f"Fixture {fixture_id} has no Home Team."
            )

        if not away_team:
            raise ValueError(
                f"Fixture {fixture_id} has no Away Team."
            )

        if not meeting_type:
            raise ValueError(
                f"Fixture {fixture_id} has no Meeting Type."
            )

        meeting_date = self._parse_date(
            data.get("Meeting Date")
        )

        return Fixture(
            fixture_id=fixture_id,
            meeting_date=meeting_date,
            home_team=home_team,
            away_team=away_team,
            meeting_type=meeting_type,
        )

    # ------------------------------------------------------------------
    # LOOKUPS
    # ------------------------------------------------------------------

    def get_fixture(
        self,
        fixture_id: str,
    ) -> Optional[Fixture]:
        """Return a fixture by ID."""

        return self.fixtures.get(
            str(fixture_id).strip()
        )

    def get_all_fixtures(self) -> List[Fixture]:
        """Return all fixtures."""

        return list(self.fixtures.values())

    def get_fixture_count(self) -> int:
        """Return the number of loaded fixtures."""

        return len(self.fixtures)

    def get_fixtures_for_team(
        self,
        team_name: str,
    ) -> List[Fixture]:
        """Return all fixtures involving a team."""

        target = self._normalise_name(
            team_name
        )

        return [
            fixture
            for fixture in self.fixtures.values()
            if (
                self._normalise_name(
                    fixture.home_team
                ) == target
                or
                self._normalise_name(
                    fixture.away_team
                ) == target
            )
        ]

    def get_home_fixtures(
        self,
        team_name: str,
    ) -> List[Fixture]:
        """Return fixtures where a team is at home."""

        target = self._normalise_name(
            team_name
        )

        return [
            fixture
            for fixture in self.fixtures.values()
            if self._normalise_name(
                fixture.home_team
            ) == target
        ]

    def get_away_fixtures(
        self,
        team_name: str,
    ) -> List[Fixture]:
        """Return fixtures where a team is away."""

        target = self._normalise_name(
            team_name
        )

        return [
            fixture
            for fixture in self.fixtures.values()
            if self._normalise_name(
                fixture.away_team
            ) == target
        ]

    def get_fixtures_on_date(
        self,
        meeting_date: date,
    ) -> List[Fixture]:
        """Return fixtures taking place on a specific date."""

        return [
            fixture
            for fixture in self.fixtures.values()
            if fixture.meeting_date == meeting_date
        ]

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    def validate_database(self) -> bool:
        """Validate the loaded fixture database."""

        if not self.fixtures:
            raise ValueError(
                "Fixture database contains no fixtures."
            )

        for fixture in self.fixtures.values():

            if not fixture.fixture_id:
                raise ValueError(
                    "Fixture has no ID."
                )

            if not fixture.home_team:
                raise ValueError(
                    f"Fixture {fixture.fixture_id} "
                    f"has no home team."
                )

            if not fixture.away_team:
                raise ValueError(
                    f"Fixture {fixture.fixture_id} "
                    f"has no away team."
                )

            if (
                self._normalise_name(
                    fixture.home_team
                )
                ==
                self._normalise_name(
                    fixture.away_team
                )
            ):
                raise ValueError(
                    f"Fixture {fixture.fixture_id} "
                    f"has the same home and away team."
                )

        return True

    # ------------------------------------------------------------------
    # DATE PARSING
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_date(value) -> date:
        """
        Convert the historical DD/MM/YYYY date format
        into a Python date object.
        """

        if value is None:
            raise ValueError(
                "Missing Meeting Date."
            )

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        text = str(value).strip()

        if not text:
            raise ValueError(
                "Meeting Date is empty."
            )

        formats = (
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
        )

        for date_format in formats:

            try:

                return datetime.strptime(
                    text,
                    date_format,
                ).date()

            except ValueError:
                continue

        raise ValueError(
            f"Invalid Meeting Date: '{value}'. "
            f"Expected DD/MM/YYYY."
        )

    # ------------------------------------------------------------------
    # TEXT HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _text(value) -> str:
        """Convert a value safely to text."""

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _normalise_name(value: str) -> str:
        """Normalise team names for reliable matching."""

        return " ".join(
            str(value).strip().lower().split()
        )


# ----------------------------------------------------------------------
# MODULE-LEVEL MANAGER
# ----------------------------------------------------------------------

fixture_database_manager = FixtureDatabaseManager()
