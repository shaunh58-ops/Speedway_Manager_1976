"""
British League Speedway Manager
Club Database Manager

Version: 0.3.1

Loads and manages the historical 1976 club database.
Aligned with the actual clubs_1976.json schema.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from core.logger import get_logger

log = get_logger("ClubDatabaseManager")


@dataclass
class Club:
    """A British League club from the 1976 database."""

    club_id: str
    name: str
    nickname: str
    stadium: str

    stadium_capacity: int = 0
    average_attendance: int = 0
    track_size: str = ""
    race_night: str = ""

    home_advantage_modifier: str = ""
    starting_bank_balance: float = 0.0
    board_expectations: str = ""
    fan_loyalty: str = ""
    rivals: str = ""

    # Runtime game values
    current_bank_balance: float = 0.0
    morale: int = 50
    active: bool = True


def _to_int(
    value,
    default: int = 0
) -> int:
    """Safely convert a value to an integer."""

    if value is None or value == "":
        return default

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _to_float(
    value,
    default: float = 0.0
) -> float:
    """Safely convert a value to a float."""

    if value is None or value == "":
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class ClubDatabaseManager:
    """Load and manage the historical 1976 club database."""

    def __init__(
        self,
        database_path=None
    ):

        self.database_path = (
            Path(database_path)
            if database_path
            else None
        )

        self.clubs: Dict[str, Club] = {}

    # --------------------------------------------------
    # DATABASE LOADING
    # --------------------------------------------------

    def load_database(
        self,
        file_path=None
    ):
        """Load clubs_1976.json."""

        path_value = (
            file_path
            or self.database_path
        )

        if path_value is None:
            raise ValueError(
                "No club database path was supplied"
            )

        path = Path(path_value)

        if not path.exists():
            raise FileNotFoundError(path)

        with path.open(
            "r",
            encoding="utf-8"
        ) as f:

            database = json.load(f)

        if not isinstance(database, dict):
            raise ValueError(
                "Club database root must be a JSON object"
            )

        records = database.get("data")

        if not isinstance(records, list):
            raise ValueError(
                "Club database must contain a 'data' list"
            )

        self.clubs.clear()

        for index, record in enumerate(
            records,
            start=1
        ):

            if not isinstance(record, dict):
                raise ValueError(
                    f"Club record {index} is not a JSON object"
                )

            club = self.create_club(record)

            if not club.club_id:
                raise ValueError(
                    f"Club record {index} has no 'ID No.' value"
                )

            if club.club_id in self.clubs:
                raise ValueError(
                    f"Duplicate club ID: {club.club_id}"
                )

            self.clubs[club.club_id] = club

        log.info(
            "Loaded %s clubs from %s",
            len(self.clubs),
            path
        )

        return self.clubs

    # --------------------------------------------------
    # CREATE CLUB
    # --------------------------------------------------

    def create_club(
        self,
        data
    ) -> Club:
        """Create a Club using the actual 1976 JSON fields."""

        starting_balance = _to_float(
            data.get(
                "Starting Bank Balance."
            )
        )

        return Club(

            club_id=str(
                data.get(
                    "ID No.",
                    ""
                )
            ).strip(),

            name=str(
                data.get(
                    "Club",
                    ""
                )
            ).strip(),

            nickname=str(
                data.get(
                    "Nickname",
                    ""
                )
            ).strip(),

            stadium=str(
                data.get(
                    "Stadium",
                    ""
                )
            ).strip(),

            stadium_capacity=_to_int(
                data.get(
                    "Stadium Capacity."
                )
            ),

            average_attendance=_to_int(
                data.get(
                    "Average Attendance."
                )
            ),

            track_size=str(
                data.get(
                    "Track Size.",
                    ""
                )
            ).strip(),

            race_night=str(
                data.get(
                    "Race Night",
                    ""
                )
            ).strip(),

            home_advantage_modifier=str(
                data.get(
                    "Home Advantage Modifier.",
                    ""
                )
            ).strip(),

            starting_bank_balance=starting_balance,

            board_expectations=str(
                data.get(
                    "Board Expectations.",
                    ""
                )
            ).strip(),

            fan_loyalty=str(
                data.get(
                    "Fan Loyalty.",
                    ""
                )
            ).strip(),

            rivals=str(
                data.get(
                    "Rivals.",
                    ""
                )
            ).strip(),

            current_bank_balance=starting_balance,
        )

    # --------------------------------------------------
    # LOOKUPS
    # --------------------------------------------------

    def get_club(
        self,
        club_id
    ) -> Optional[Club]:

        return self.clubs.get(
            str(club_id)
        )

    # --------------------------------------------------

    def get_club_by_name(
        self,
        name
    ) -> Optional[Club]:

        target = str(
            name
        ).strip().casefold()

        for club in self.clubs.values():

            if club.name.casefold() == target:
                return club

        return None

    # --------------------------------------------------

    def get_clubs(self) -> List[Club]:

        return list(
            self.clubs.values()
        )

    # --------------------------------------------------
    # FINANCE
    # --------------------------------------------------

    def update_balance(
        self,
        club_id,
        amount
    ):

        club = self.get_club(
            club_id
        )

        if club is None:
            return

        club.current_bank_balance += _to_float(
            amount
        )

    # --------------------------------------------------

    def get_balance(
        self,
        club_id
    ) -> float:

        club = self.get_club(
            club_id
        )

        if club is None:
            return 0.0

        return club.current_bank_balance

    # --------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------

    def get_average_attendance(
        self,
        club_id
    ) -> int:

        club = self.get_club(
            club_id
        )

        if club is None:
            return 0

        return club.average_attendance

    # --------------------------------------------------
    # RIVALS
    # --------------------------------------------------

    def get_rivals(
        self,
        club_id
    ) -> List[str]:

        club = self.get_club(
            club_id
        )

        if club is None:
            return []

        if not club.rivals:
            return []

        return [
            rival.strip()
            for rival in club.rivals.split(",")
            if rival.strip()
        ]

    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    def export_database(
        self,
        file_path
    ):

        records = []

        for club in self.clubs.values():

            records.append(
                {
                    "ID No.": club.club_id,
                    "Club": club.name,
                    "Nickname": club.nickname,
                    "Stadium": club.stadium,
                    "Stadium Capacity.": club.stadium_capacity,
                    "Average Attendance.": club.average_attendance,
                    "Track Size.": club.track_size,
                    "Race Night": club.race_night,
                    "Home Advantage Modifier.": (
                        club.home_advantage_modifier
                    ),
                    "Starting Bank Balance.": (
                        club.starting_bank_balance
                    ),
                    "Board Expectations.": (
                        club.board_expectations
                    ),
                    "Fan Loyalty.": club.fan_loyalty,
                    "Rivals.": club.rivals,
                }
            )

        output = {
            "data": records
        }

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


club_database_manager = ClubDatabaseManager()