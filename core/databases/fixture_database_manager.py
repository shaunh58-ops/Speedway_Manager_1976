"""
Speedway Manager 1976
Fixture Database Manager

Version: 0.3.1

Matches the actual fixtures_1976.json schema.

JSON structure:

[
    {
        "Meeting Date": "19/03/1976",
        "Home Team": "Hackney",
        "Away Team": "Newport",
        "Meeting Type": "British League"
    }
]
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Fixture:
    """Historical 1976 Speedway fixture."""

    fixture_id: str
    meeting_date: str
    home_team: str
    away_team: str
    meeting_type: str

    completed: bool = False
    home_score: int = 0
    away_score: int = 0

    @property
    def date(self) -> str:
        return self.meeting_date

    @property
    def competition(self) -> str:
        return self.meeting_type


class FixtureDatabaseManager:
    """Loads and manages the 1976 fixture database."""

    def __init__(
        self,
        database_path=None
    ):
        self.database_path = (
            Path(database_path)
            if database_path
            else None
        )

        self.fixtures: Dict[str, Fixture] = {}

    # ======================================================
    # LOAD DATABASE
    # ======================================================

    def load_database(
        self,
        file_path=None
    ):
        """Load all historical fixtures."""

        path = Path(
            file_path or self.database_path
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Fixture database not found: {path}"
            )

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(
                "Fixture database must contain a JSON list"
            )

        self.fixtures.clear()

        for index, record in enumerate(
            records,
            start=1
        ):
            fixture = self._create_fixture(
                record,
                index
            )

            self.fixtures[
                fixture.fixture_id
            ] = fixture

        return self.fixtures

    # ======================================================
    # CREATE FIXTURE
    # ======================================================

    def _create_fixture(
        self,
        record,
        index
    ) -> Fixture:
        """Convert one JSON record into a Fixture."""

        if not isinstance(record, dict):
            raise ValueError(
                f"Fixture record {index} is not an object"
            )

        meeting_date = str(
            record.get(
                "Meeting Date",
                ""
            )
        ).strip()

        home_team = str(
            record.get(
                "Home Team",
                ""
            )
        ).strip()

        away_team = str(
            record.get(
                "Away Team",
                ""
            )
        ).strip()

        meeting_type = str(
            record.get(
                "Meeting Type",
                ""
            )
        ).strip()

        if not meeting_date:
            raise ValueError(
                f"Fixture {index} has no Meeting Date"
            )

        if not home_team:
            raise ValueError(
                f"Fixture {index} has no Home Team"
            )

        if not away_team:
            raise ValueError(
                f"Fixture {index} has no Away Team"
            )

        fixture_id = (
            f"FIX-{index:04d}"
        )

        return Fixture(
            fixture_id=fixture_id,
            meeting_date=meeting_date,
            home_team=home_team,
            away_team=away_team,
            meeting_type=meeting_type
        )

    # ======================================================
    # BASIC LOOKUPS
    # ======================================================

    def get_fixture(
        self,
        fixture_id
    ) -> Optional[Fixture]:

        return self.fixtures.get(
            str(fixture_id)
        )

    # ======================================================

    def get_all_fixtures(
        self
    ) -> List[Fixture]:

        return list(
            self.fixtures.values()
        )

    # ======================================================
    # TEAM LOOKUPS
    # ======================================================

    def get_fixtures_by_team(
        self,
        team_name
    ) -> List[Fixture]:

        target = str(
            team_name
        ).strip().casefold()

        return [
            fixture
            for fixture in self.fixtures.values()
            if (
                fixture.home_team.casefold()
                == target
                or
                fixture.away_team.casefold()
                == target
            )
        ]

    # ======================================================

    def get_home_fixtures(
        self,
        team_name
    ) -> List[Fixture]:

        target = str(
            team_name
        ).strip().casefold()

        return [
            fixture
            for fixture in self.fixtures.values()
            if fixture.home_team.casefold()
            == target
        ]

    # ======================================================

    def get_away_fixtures(
        self,
        team_name
    ) -> List[Fixture]:

        target = str(
            team_name
        ).strip().casefold()

        return [
            fixture
            for fixture in self.fixtures.values()
            if fixture.away_team.casefold()
            == target
        ]

    # ======================================================
    # DATE LOOKUPS
    # ======================================================

    def get_fixtures_by_date(
        self,
        meeting_date
    ) -> List[Fixture]:

        target = str(
            meeting_date
        ).strip()

        return [
            fixture
            for fixture in self.fixtures.values()
            if fixture.meeting_date == target
        ]

    # ======================================================
    # COMPETITION LOOKUPS
    # ======================================================

    def get_fixtures_by_type(
        self,
        meeting_type
    ) -> List[Fixture]:

        target = str(
            meeting_type
        ).strip().casefold()

        return [
            fixture
            for fixture in self.fixtures.values()
            if fixture.meeting_type.casefold()
            == target
        ]

    # ======================================================
    # DATE SORTING
    # ======================================================

    def get_fixtures_sorted(
        self
    ) -> List[Fixture]:

        return sorted(
            self.fixtures.values(),
            key=lambda fixture:
                self._parse_date(
                    fixture.meeting_date
                )
        )

    # ======================================================
    # DATE RANGE
    # ======================================================

    def get_fixtures_by_date_range(
        self,
        start_date,
        end_date
    ) -> List[Fixture]:

        start = self._parse_date(
            start_date
        )

        end = self._parse_date(
            end_date
        )

        return [
            fixture
            for fixture in self.fixtures.values()
            if (
                start
                <= self._parse_date(
                    fixture.meeting_date
                )
                <= end
            )
        ]

    # ======================================================
    # RESULT MANAGEMENT
    # ======================================================

    def record_result(
        self,
        fixture_id,
        home_score,
        away_score
    ):

        fixture = self.get_fixture(
            fixture_id
        )

        if fixture is None:
            raise ValueError(
                f"Unknown fixture: {fixture_id}"
            )

        fixture.home_score = int(
            home_score
        )

        fixture.away_score = int(
            away_score
        )

        fixture.completed = True

    # ======================================================
    # DATE PARSER
    # ======================================================

    @staticmethod
    def _parse_date(
        value
    ):

        if isinstance(
            value,
            datetime
        ):
            return value

        return datetime.strptime(
            str(value).strip(),
            "%d/%m/%Y"
        )


fixture_database_manager = (
    FixtureDatabaseManager()
)