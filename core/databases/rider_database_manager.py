"""
British League Speedway Manager
Rider Database Manager

Version: 0.3.1

Loads and manages the historical 1976 rider database.
The loader is aligned with the actual riders_1976.json schema.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from core.logger import get_logger

log = get_logger("RiderDatabaseManager")


@dataclass
class Rider:
    """A rider loaded from the historical 1976 database."""

    rider_id: str
    name: str
    club: str
    age: int = 0
    nationality: str = ""
    cma: float = 0.0

    gating: int = 0
    cornering: int = 0
    passing: int = 0
    consistency: int = 0
    fitness: int = 0
    injury_risk: int = 0
    home_track_rating: int = 0
    potential: int = 0
    retirement_age: int = 0
    career_notes: str = ""

    # Runtime statistics
    experience: int = 50
    morale: int = 50
    injury_days: int = 0
    active: bool = True
    meetings: int = 0
    rides: int = 0
    points: int = 0
    bonus_points: int = 0
    average: float = 0.0

    @property
    def starting_average(self) -> float:
        """Compatibility alias for the historical CMA."""
        return self.cma


def _to_int(value, default: int = 0) -> int:
    """Safely convert a JSON value to an integer."""

    if value is None or value == "":
        return default

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _to_float(value, default: float = 0.0) -> float:
    """Safely convert a JSON value to a float."""

    if value is None or value == "":
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class RiderDatabaseManager:
    """Load and manage the historical 1976 rider database."""

    def __init__(self, database_path=None):
        self.database_path = (
            Path(database_path)
            if database_path
            else None
        )

        self.riders: Dict[str, Rider] = {}

    # --------------------------------------------------
    # DATABASE LOADING
    # --------------------------------------------------

    def load_database(self, file_path=None):
        """Load riders_1976.json using the actual historical JSON schema."""

        path_value = file_path or self.database_path

        if path_value is None:
            raise ValueError(
                "No rider database path was supplied"
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
                f"Rider database must contain a JSON list: {path}"
            )

        self.riders.clear()

        for index, record in enumerate(
            records,
            start=1
        ):

            if not isinstance(record, dict):
                raise ValueError(
                    f"Rider record {index} is not a JSON object"
                )

            rider = self.create_rider(record)

            if not rider.rider_id:
                raise ValueError(
                    f"Rider record {index} has no 'Rider ID' value"
                )

            if rider.rider_id in self.riders:
                raise ValueError(
                    f"Duplicate Rider ID found: {rider.rider_id}"
                )

            self.riders[rider.rider_id] = rider

        log.info(
            "Loaded %s riders from %s",
            len(self.riders),
            path
        )

        return self.riders

    # --------------------------------------------------
    # CREATE RIDER
    # --------------------------------------------------

    def create_rider(self, data) -> Rider:
        """Create a Rider from the actual 1976 JSON field names."""

        return Rider(

            rider_id=str(
                data.get(
                    "Rider ID",
                    ""
                )
            ).strip(),

            name=str(
                data.get(
                    "Name",
                    "Unknown Rider"
                )
            ).strip(),

            club=str(
                data.get(
                    "Team",
                    ""
                )
            ).strip(),

            age=_to_int(
                data.get(
                    "Age (1976)"
                )
            ),

            nationality=str(
                data.get(
                    "Nationality",
                    ""
                )
            ).strip(),

            cma=_to_float(
                data.get(
                    "CMA"
                )
            ),

            gating=_to_int(
                data.get(
                    "Gating"
                )
            ),

            cornering=_to_int(
                data.get(
                    "Cornering"
                )
            ),

            passing=_to_int(
                data.get(
                    "Passing"
                )
            ),

            consistency=_to_int(
                data.get(
                    "Consistency"
                )
            ),

            fitness=_to_int(
                data.get(
                    "Fitness"
                )
            ),

            injury_risk=_to_int(
                data.get(
                    "Injury Risk"
                )
            ),

            home_track_rating=_to_int(
                data.get(
                    "Home Track Rating"
                )
            ),

            potential=_to_int(
                data.get(
                    "Potential"
                )
            ),

            retirement_age=_to_int(
                data.get(
                    "Retirement Age"
                )
            ),

            career_notes=str(
                data.get(
                    "Career Notes",
                    ""
                )
            ).strip(),
        )

    # --------------------------------------------------
    # LOOKUPS
    # --------------------------------------------------

    def get_rider(
        self,
        rider_id
    ) -> Optional[Rider]:

        return self.riders.get(
            str(rider_id)
        )

    # --------------------------------------------------

    def get_rider_by_name(
        self,
        name
    ) -> Optional[Rider]:

        target = str(
            name
        ).strip().casefold()

        for rider in self.riders.values():

            if rider.name.casefold() == target:
                return rider

        return None

    # --------------------------------------------------

    def get_club_riders(
        self,
        club_name
    ) -> List[Rider]:

        target = str(
            club_name
        ).strip().casefold()

        return sorted(

            [
                rider

                for rider in self.riders.values()

                if rider.club.casefold() == target
            ],

            key=lambda rider: rider.cma,

            reverse=True
        )

    # --------------------------------------------------
    # RACE STATISTICS
    # --------------------------------------------------

    def update_statistics(
        self,
        rider_id,
        rides,
        points,
        bonus
    ):

        rider = self.get_rider(
            rider_id
        )

        if rider is None:
            return

        rider.meetings += 1

        rider.rides += _to_int(
            rides
        )

        rider.points += _to_int(
            points
        )

        rider.bonus_points += _to_int(
            bonus
        )

        total = (
            rider.points
            + rider.bonus_points
        )

        rider.average = (
            total / rider.rides
            if rider.rides
            else 0.0
        )

    # --------------------------------------------------
    # INJURY
    # --------------------------------------------------

    def injure_rider(
        self,
        rider_id,
        days
    ):

        rider = self.get_rider(
            rider_id
        )

        if rider:

            rider.injury_days = max(
                0,
                _to_int(days)
            )

            if rider.injury_days:
                rider.fitness = 0

    # --------------------------------------------------

    def advance_day(self):

        for rider in self.riders.values():

            if rider.injury_days > 0:

                rider.injury_days -= 1

                if rider.injury_days == 0:
                    rider.fitness = 100

    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    def export_database(
        self,
        file_path
    ):

        output = [
            rider.__dict__.copy()
            for rider in self.riders.values()
        ]

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                output,
                f,
                indent=4,
                ensure_ascii=False
            )


rider_database_manager = RiderDatabaseManager()