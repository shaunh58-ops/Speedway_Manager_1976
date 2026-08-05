"""
British League Speedway Manager
Fixture Database Manager

Version: 0.3.1

Loads and manages the historical 1976 fixture database.
Aligned with the actual fixtures_1976.json schema.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from core.logger import get_logger

log = get_logger("FixtureDatabaseManager")


@dataclass
class Fixture:
    """A historical Speedway fixture."""

    fixture_id: str
    meeting_date: str
    home_team: str
    away_team: str
    meeting_type: str

    # Runtime status
    completed: bool = False
    home_score: int = 0
    away_score: int = 0

    @property
    def date(self) -> str:
        """Compatibility alias for meeting_date."""
        return self.meeting_date

    @property
    def competition(self) -> str:
        """Compatibility alias for meeting_type."""
        return self.meeting_type


class FixtureDatabaseManager:
    """Load and manage the historical 1976 fixture database."""

    def __init__(
        self,
        database_path=None
    ):

        self.database_path = (
            Path(database_path)
            if database_path
            else None
        )

        self.fixtures: List[Fixture] = []

    # --------------------------------------------------
    # DATABASE LOADING
    # --------------------------------------------------

    def load_database(
        self,
        file_path=None
    ):
        """Load fixtures_1976.json."""

        path_value = (
            file_path
            or self.database_path
        )

        if path_value is None:
            raise ValueError(
                "No fixture database path was supplied"
            )

        path = Path(path_value)

        if not path.exists():
            raise FileNotFoundError(path)

        with path.open(
            "r",
            encoding="utf-8"
        ) as f:

            records = json.load(f)

        if not isinstance(records, list):
            raise ValueError(
                "Fixture database root must be a JSON list"
            )

        self.fixtures.clear()

        for index, record in enumerate(
            records,
            start=1
        ):

            if not isinstance(record, dict):
                raise ValueError(
                    f"Fixture record {index} "
                    "is not a JSON object"
                )

            fixture = self.create_fixture(
                record,
                index
            )

            self.fixtures.append(
                fixture
            )

        log.info(
            "Loaded %s fixtures from %s",
            len(self.fixtures),
            path
        )

        return self.fixtures

    # --------------------------------------------------
    # CREATE FIXTURE
    # --------------------------------------------------

    def create_fixture(
        self,
        data,
        index: int
    ) -> Fixture:
        """Create a Fixture using the actual 1976 JSON fields."""

        meeting_date = str(
            data.get(
                "Meeting Date",
                ""
            )
        ).strip()

        home_team = str(
            data.get(
                "Home Team",
                ""
            )
        ).strip()

        away_team = str(
            data.get(
                "Away Team",
                ""
            )
        ).strip()

        meeting_type = str(
            data.get(
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

        return Fixture(

            fixture_id=f"FIX-{index:04d}",

            meeting_date=meeting_date,

            home_team=home_team,

            away_team=away_team,

            meeting_type=meeting_type,
        )

    # --------------------------------------------------
    # LOOKUPS
    # --------------------------------------------------

    def get_fixture(
        self,
        fixture_id
    ) -> Optional[Fixture]:

        target = str(
            fixture_id
        )

        for fixture in self.fixtures:

            if fixture.fixture_id == target:
                return fixture

        return None

    # --------------------------------------------------

    def get_all_fixtures(
        self
    ) -> List[Fixture]:

        return list(
            self.fixtures
        )

    # --------------------------------------------------

    def get_fixtures_by_team(
        self,
        team_name
    ) -> List[Fixture]:

        target = str(
            team_name
        ).strip().casefold()

        return [

            fixture

            for fixture in self.fixtures

            if (
                fixture.home_team.casefold()
                == target
                or
                fixture.away_team.casefold()
                == target
            )
        ]

    # --------------------------------------------------

    def get_home_fixtures(
        self,
        team_name
    ) -> List[Fixture]:

        target = str(
            team_name
        ).strip().casefold()

        return [

            fixture

            for fixture in self.fixtures

            if fixture.home_team.casefold()
            == target
        ]

    # --------------------------------------------------

    def get_away_fixtures(
        self,
        team_name
    ) -> List[Fixture]:

        target = str(
            team_name
        ).strip().casefold()

        return [

            fixture

            for fixture in self.fixtures

            if fixture.away_team.casefold()
            == target
        ]

    # --------------------------------------------------
    # DATE LOOKUPS
    # --------------------------------------------------

    def get_fixtures_by_date(
        self,
        meeting_date
    ) -> List[Fixture]:

        target = str(
            meeting_date
        ).strip()

        return [

            fixture

            for fixture in self.fixtures

            if fixture.meeting_date == target
        ]

    # --------------------------------------------------

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

        results = []

        for fixture in self.fixtures:

            fixture_date = self._parse_date(
                fixture.meeting_date
            )

            if (
                start
                <= fixture_date
                <= end
            ):

                results.append(
                    fixture
                )

        return results

    # --------------------------------------------------
    # COMPETITION LOOKUPS
    # --------------------------------------------------

    def get_fixtures_by_type(
        self,
        meeting_type
    ) -> List[Fixture]:

        target = str(
            meeting_type
        ).strip().casefold()

        return [

            fixture

            for fixture in self.fixtures

            if fixture.meeting_type.casefold()
            == target
        ]

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

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

    # --------------------------------------------------
    # DATE SORTING
    # --------------------------------------------------

    def get_fixtures_sorted(
        self
    ) -> List[Fixture]:

        return sorted(
            self.fixtures,
            key=lambda fixture:
                self._parse_date(
                    fixture.meeting_date
                )
        )

    # --------------------------------------------------
    # INTERNAL DATE PARSER
    # --------------------------------------------------

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

    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    def export_database(
        self,
        file_path
    ):

        output = []

        for fixture in self.fixtures:

            output.append(
                {
                    "Meeting Date":
                        fixture.meeting_date,

                    "Home Team":
                        fixture.home_team,

                    "Away Team":
                        fixture.away_team,

                    "Meeting Type":
                        fixture.meeting_type,
                }
            )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                output,
                f,
                indent=2,
                ensure_ascii=False
            )


fixture_database_manager = (
    FixtureDatabaseManager()
)