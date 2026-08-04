"""
Club Database Manager
Speedway Manager 1976

Loads and manages the historical 1976 club database.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

from core.logger import get_logger


log = get_logger("ClubDatabaseManager")


@dataclass
class Club:
    """Represents a Speedway club during the 1976 season."""

    club_id: str
    name: str
    nickname: str
    stadium: str

    stadium_capacity: int
    average_attendance: int
    track_size: float

    race_night: str
    home_advantage_modifier: str

    starting_bank_balance: float
    board_expectations: str
    fan_loyalty: str
    rivals: List[str]

    # Riders are assigned by WorldBuilder after both
    # the club and rider databases have been loaded.
    riders: List[str] | None = None

    # Dynamic game data
    league_points: int = 0
    meetings: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    points_for: int = 0
    points_against: int = 0

    @property
    def points_difference(self) -> int:
        """Return points scored minus points conceded."""

        return self.points_for - self.points_against


class ClubDatabaseManager:
    """Loads and provides access to the 1976 club database."""

    def __init__(
        self,
        database_path: Optional[Union[str, Path]] = None,
    ) -> None:

        self.database_path = (
            Path(database_path)
            if database_path is not None
            else None
        )

        self.clubs: Dict[str, Club] = {}

    # ------------------------------------------------------------------
    # DATABASE LOADING
    # ------------------------------------------------------------------

    def load_database(
        self,
        file_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Club]:
        """
        Load the historical club database.

        Your 1976 club JSON uses:

        {
            "data": [
                {...},
                {...}
            ]
        }
        """

        path = Path(file_path) if file_path else self.database_path

        if path is None:
            raise ValueError(
                "No club database path has been supplied."
            )

        if not path.exists():
            raise FileNotFoundError(
                f"Club database not found: {path}"
            )

        log.info("Loading club database: %s", path)

        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        records = self._extract_records(raw_data)

        self.clubs.clear()

        for record_number, record in enumerate(records, start=1):

            try:
                club = self.create_club(record)

                if not club.club_id:
                    raise ValueError(
                        "Club has no ID No."
                    )

                if club.club_id in self.clubs:
                    raise ValueError(
                        f"Duplicate club ID: {club.club_id}"
                    )

                self.clubs[club.club_id] = club

            except Exception as exc:

                raise ValueError(
                    f"Error loading club record "
                    f"{record_number}: {exc}"
                ) from exc

        log.info(
            "Successfully loaded %s clubs.",
            len(self.clubs),
        )

        return self.clubs

    # ------------------------------------------------------------------
    # RECORD EXTRACTION
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_records(raw_data) -> List[dict]:
        """Extract club records from the JSON structure."""

        if not isinstance(raw_data, dict):
            raise ValueError(
                "Club database must contain a JSON object."
            )

        records = raw_data.get("data")

        if not isinstance(records, list):
            raise ValueError(
                "Club database must contain a 'data' list."
            )

        return records

    # ------------------------------------------------------------------
    # CLUB CREATION
    # ------------------------------------------------------------------

    def create_club(self, data: dict) -> Club:
        """Convert one historical JSON record into a Club object."""

        club_id = self._text(
            data.get("ID No.")
        )

        name = self._text(
            data.get("Club")
        )

        nickname = self._text(
            data.get("Nickname")
        )

        stadium = self._text(
            data.get("Stadium")
        )

        if not club_id:
            raise ValueError(
                "Missing 'ID No.'."
            )

        if not name:
            raise ValueError(
                f"Club {club_id} is missing 'Club'."
            )

        if not stadium:
            raise ValueError(
                f"Club {club_id} is missing 'Stadium'."
            )

        club = Club(
            club_id=club_id,
            name=name,
            nickname=nickname,
            stadium=stadium,

            stadium_capacity=self._integer(
                data.get("Stadium Capacity.")
            ),

            average_attendance=self._integer(
                data.get("Average Attendance.")
            ),

            track_size=self._track_size(
                data.get("Track Size.")
            ),

            race_night=self._text(
                data.get("Race Night")
            ),

            home_advantage_modifier=self._text(
                data.get("Home Advantage Modifier.")
            ),

            starting_bank_balance=self._number(
                data.get("Starting Bank Balance.")
            ),

            board_expectations=self._text(
                data.get("Board Expectations.")
            ),

            fan_loyalty=self._text(
                data.get("Fan Loyalty.")
            ),

            rivals=self._parse_rivals(
                data.get("Rivals.")
            ),

            riders=[],
        )

        return club

    # ------------------------------------------------------------------
    # LOOKUPS
    # ------------------------------------------------------------------

    def get_club(
        self,
        club_id: str,
    ) -> Optional[Club]:
        """Return a club using its database ID."""

        return self.clubs.get(
            str(club_id).strip()
        )

    def get_club_by_name(
        self,
        club_name: str,
    ) -> Optional[Club]:
        """Return a club using its name."""

        target = self._normalise_name(
            club_name
        )

        for club in self.clubs.values():

            if self._normalise_name(
                club.name
            ) == target:
                return club

        return None

    def get_all_clubs(self) -> List[Club]:
        """Return all clubs as a list."""

        return list(self.clubs.values())

    def get_club_count(self) -> int:
        """Return the number of loaded clubs."""

        return len(self.clubs)

    # ------------------------------------------------------------------
    # RIDER ASSIGNMENT
    # ------------------------------------------------------------------

    def assign_riders(
        self,
        club_id: str,
        rider_ids: List[str],
    ) -> None:
        """
        Assign rider IDs to a club.

        WorldBuilder should perform the actual historical
        rider-to-team matching.
        """

        club = self.get_club(club_id)

        if club is None:
            raise ValueError(
                f"Club not found: {club_id}"
            )

        club.riders = list(rider_ids)

    def add_rider(
        self,
        club_id: str,
        rider_id: str,
    ) -> None:
        """Add one rider ID to a club."""

        club = self.get_club(club_id)

        if club is None:
            raise ValueError(
                f"Club not found: {club_id}"
            )

        if club.riders is None:
            club.riders = []

        rider_id = str(rider_id)

        if rider_id not in club.riders:
            club.riders.append(rider_id)

    def get_club_rider_ids(
        self,
        club_id: str,
    ) -> List[str]:
        """Return the rider IDs assigned to a club."""

        club = self.get_club(club_id)

        if club is None:
            return []

        return list(club.riders or [])

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    def validate_database(self) -> bool:
        """Validate the loaded club database."""

        if not self.clubs:
            raise ValueError(
                "Club database contains no clubs."
            )

        for club in self.clubs.values():

            if not club.club_id:
                raise ValueError(
                    "A club is missing its ID."
                )

            if not club.name:
                raise ValueError(
                    f"Club {club.club_id} has no name."
                )

            if not club.stadium:
                raise ValueError(
                    f"Club {club.name} has no stadium."
                )

            if club.stadium_capacity <= 0:
                raise ValueError(
                    f"Invalid stadium capacity for "
                    f"{club.name}."
                )

            if club.track_size <= 0:
                raise ValueError(
                    f"Invalid track size for "
                    f"{club.name}."
                )

        return True

    # ------------------------------------------------------------------
    # DATA CONVERSION HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _text(value) -> str:
        """Convert a value safely to text."""

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _number(value) -> float:
        """Convert a numeric value or numeric string to float."""

        if value is None:
            return 0.0

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()

        if not text:
            return 0.0

        # Remove currency symbols and commas.
        text = text.replace(",", "")
        text = text.replace("£", "")

        match = re.search(
            r"-?\d+(?:\.\d+)?",
            text,
        )

        if not match:
            raise ValueError(
                f"Cannot convert '{value}' to a number."
            )

        return float(match.group())

    @classmethod
    def _integer(cls, value) -> int:
        """Convert a value to an integer."""

        return int(
            round(
                cls._number(value)
            )
        )

    @classmethod
    def _track_size(cls, value) -> float:
        """
        Convert track sizes such as:

        '382m'
        '360 m'
        '382'
        
        into metres.
        """

        return cls._number(value)

    @staticmethod
    def _parse_rivals(value) -> List[str]:
        """Convert the comma-separated Rivals field into a list."""

        if value is None:
            return []

        if isinstance(value, list):
            return [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

        return [
            item.strip()
            for item in str(value).split(",")
            if item.strip()
        ]

    @staticmethod
    def _normalise_name(value: str) -> str:
        """Normalise names for reliable matching."""

        return " ".join(
            str(value).strip().lower().split()
        )


# ----------------------------------------------------------------------
# MODULE-LEVEL MANAGER
# ----------------------------------------------------------------------

club_database_manager = ClubDatabaseManager()
