"""
Rider Database Manager
Speedway Manager 1976

Loads and manages the historical 1976 rider database.

The JSON database contains historical starting data.
Season statistics such as meetings, rides and points are
maintained by the game and are not stored in the historical JSON.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

from core.logger import get_logger


log = get_logger("RiderDatabaseManager")


@dataclass
class Rider:
    """Represents a rider entering the 1976 season."""

    rider_id: str
    name: str
    club: str
    nationality: str

    # Historical starting data
    age: int
    cma: float
    gating: float
    cornering: float
    passing: float
    consistency: float
    fitness: float
    injury_risk: float
    home_track_rating: float
    potential: float
    retirement_age: int
    career_notes: str

    # Dynamic season data
    meetings: int = 0
    rides: int = 0
    points: int = 0
    bonus_points: int = 0
    injured: bool = False

    @property
    def average(self) -> float:
        """
        Calculate the rider's current season average.

        If the rider has not yet ridden a meeting then the
        historical starting CMA is returned.
        """
        if self.rides > 0:
            return self.points / self.rides

        return self.cma


class RiderDatabaseManager:
    """Loads and provides access to the 1976 rider database."""

    def __init__(
        self,
        database_path: Optional[Union[str, Path]] = None,
    ) -> None:

        self.database_path = (
            Path(database_path)
            if database_path is not None
            else None
        )

        self.riders: Dict[str, Rider] = {}

    # ------------------------------------------------------------------
    # DATABASE LOADING
    # ------------------------------------------------------------------

    def load_database(
        self,
        file_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Rider]:
        """
        Load the historical rider database.

        Supports either:

        [
            {...},
            {...}
        ]

        or:

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
                "No rider database path has been supplied."
            )

        if not path.exists():
            raise FileNotFoundError(
                f"Rider database not found: {path}"
            )

        log.info("Loading rider database: %s", path)

        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        records = self._extract_records(raw_data)

        self.riders.clear()

        for record_number, record in enumerate(records, start=1):

            try:
                rider = self.create_rider(record)

                if not rider.rider_id:
                    raise ValueError(
                        "Rider has no Rider ID."
                    )

                if rider.rider_id in self.riders:
                    raise ValueError(
                        f"Duplicate Rider ID: {rider.rider_id}"
                    )

                self.riders[rider.rider_id] = rider

            except Exception as exc:
                raise ValueError(
                    f"Error loading rider record "
                    f"{record_number}: {exc}"
                ) from exc

        log.info(
            "Successfully loaded %s riders.",
            len(self.riders),
        )

        return self.riders

    # ------------------------------------------------------------------
    # RECORD EXTRACTION
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_records(raw_data) -> List[dict]:
        """Extract rider records from supported JSON structures."""

        if isinstance(raw_data, list):
            records = raw_data

        elif isinstance(raw_data, dict):
            records = raw_data.get("data")

        else:
            records = None

        if not isinstance(records, list):
            raise ValueError(
                "Rider database must contain a JSON list "
                "or an object containing a 'data' list."
            )

        return records

    # ------------------------------------------------------------------
    # RIDER CREATION
    # ------------------------------------------------------------------

    def create_rider(self, data: dict) -> Rider:
        """Convert one historical JSON record into a Rider object."""

        rider_id = self._text(
            data.get("Rider ID")
        )

        name = self._text(
            data.get("Name")
        )

        club = self._text(
            data.get("Team")
        )

        nationality = self._text(
            data.get("Nationality")
        )

        if not rider_id:
            raise ValueError("Missing 'Rider ID'.")

        if not name:
            raise ValueError(
                f"Rider {rider_id} is missing 'Name'."
            )

        if not club:
            raise ValueError(
                f"Rider {rider_id} is missing 'Team'."
            )

        rider = Rider(
            rider_id=rider_id,
            name=name,
            club=club,
            nationality=nationality,

            age=self._integer(
                data.get("Age (1976)")
            ),

            cma=self._number(
                data.get("CMA")
            ),

            gating=self._number(
                data.get("Gating")
            ),

            cornering=self._number(
                data.get("Cornering")
            ),

            passing=self._number(
                data.get("Passing")
            ),

            consistency=self._number(
                data.get("Consistency")
            ),

            fitness=self._number(
                data.get("Fitness")
            ),

            injury_risk=self._number(
                data.get("Injury Risk")
            ),

            home_track_rating=self._number(
                data.get("Home Track Rating")
            ),

            potential=self._number(
                data.get("Potential")
            ),

            retirement_age=self._integer(
                data.get("Retirement Age")
            ),

            career_notes=self._text(
                data.get("Career Notes")
            ),
        )

        return rider

    # ------------------------------------------------------------------
    # LOOKUPS
    # ------------------------------------------------------------------

    def get_rider(
        self,
        rider_id: str,
    ) -> Optional[Rider]:
        """Return a rider by Rider ID."""

        return self.riders.get(str(rider_id))

    def get_rider_by_name(
        self,
        name: str,
    ) -> Optional[Rider]:
        """Return a rider by exact name match."""

        target = self._text(name).lower()

        for rider in self.riders.values():

            if rider.name.lower() == target:
                return rider

        return None

    def get_club_riders(
        self,
        club_name: str,
    ) -> List[Rider]:
        """Return all riders belonging to a club."""

        target = self._normalise_name(club_name)

        return [
            rider
            for rider in self.riders.values()
            if self._normalise_name(rider.club) == target
        ]

    def get_all_riders(self) -> List[Rider]:
        """Return all riders as a list."""

        return list(self.riders.values())

    def get_rider_count(self) -> int:
        """Return the number of loaded riders."""

        return len(self.riders)

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    def validate_database(self) -> bool:
        """
        Validate the loaded rider database.

        Returns True when all loaded riders contain the
        minimum required historical information.
        """

        if not self.riders:
            raise ValueError(
                "Rider database contains no riders."
            )

        for rider in self.riders.values():

            if not rider.rider_id:
                raise ValueError(
                    "A rider is missing a Rider ID."
                )

            if not rider.name:
                raise ValueError(
                    f"Rider {rider.rider_id} has no name."
                )

            if not rider.club:
                raise ValueError(
                    f"Rider {rider.rider_id} has no club."
                )

            if rider.age <= 0:
                raise ValueError(
                    f"Invalid age for rider "
                    f"{rider.name}: {rider.age}"
                )

            if rider.cma < 0:
                raise ValueError(
                    f"Invalid CMA for rider "
                    f"{rider.name}: {rider.cma}"
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
        """
        Convert numeric strings such as:

        '7.56'
        '85'
        '85.0'

        into floats.
        """

        if value is None:
            return 0.0

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()

        if not text:
            return 0.0

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
        """Convert a value safely to an integer."""

        return int(cls._number(value))

    @staticmethod
    def _normalise_name(value: str) -> str:
        """
        Normalise club names for matching.

        This prevents simple differences in spacing and case
        from breaking rider-to-club matching.
        """

        return " ".join(
            str(value).strip().lower().split()
        )


# ----------------------------------------------------------------------
# MODULE-LEVEL MANAGER
# ----------------------------------------------------------------------

rider_database_manager = RiderDatabaseManager()
