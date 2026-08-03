"""
British League Speedway Manager

Rider Database Manager

Version: 1.0

Loads and manages historical rider data.
"""

from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional

from core.logger import get_logger

log = get_logger("RiderDatabaseManager")


@dataclass
class Rider:

    rider_id: str

    name: str

    club: str

    nationality: str = ""

    age: int = 0

    cma: float = 0.0

    starting_average: float = 0.0

    experience: int = 50

    morale: int = 50

    fitness: int = 100

    injury_days: int = 0

    active: bool = True

    meetings: int = 0

    rides: int = 0

    points: int = 0

    bonus_points: int = 0

    average: float = 0.0


class RiderDatabaseManager:

    def __init__(self, database_path=None):

        self.database_path = database_path

        self.riders: Dict[str, Rider] = {}

    # --------------------------------------------------

    def load_database(self, file_path=None):

        path = Path(file_path or self.database_path)

        if not path.exists():
            raise FileNotFoundError(path)

        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)

        self.riders.clear()

        for record in records:

            rider = self.create_rider(record)

            self.riders[rider.rider_id] = rider

        log.info("Loaded %s riders", len(self.riders))

        return self.riders

    # --------------------------------------------------

    def create_rider(self, data):

        """
        Replace the field names below with the exact
        names used in your Rider JSON.
        """

        return Rider(

            rider_id=str(
                data.get(
                    "ID No.",
                    data.get(
                        "id",
                        ""
                    )
                )
            ),

            name=data.get(
                "Rider",
                data.get(
                    "Name",
                    "Unknown Rider"
                )
            ),

            club=data.get(
                "Club",
                ""
            ),

            nationality=data.get(
                "Nationality",
                ""
            ),

            age=int(
                data.get(
                    "Age",
                    0
                )
            ),

            cma=float(
                data.get(
                    "CMA",
                    0.0
                )
            ),

            starting_average=float(
                data.get(
                    "CMA",
                    0.0
                )
            )
        )

    # --------------------------------------------------

    def get_rider(
        self,
        rider_id,
    ) -> Optional[Rider]:

        return self.riders.get(str(rider_id))

    # --------------------------------------------------

    def get_rider_by_name(
        self,
        name,
    ) -> Optional[Rider]:

        for rider in self.riders.values():

            if rider.name.lower() == name.lower():

                return rider

        return None

    # --------------------------------------------------

    def get_club_riders(
        self,
        club_name,
    ) -> List[Rider]:

        return sorted(

            [

                rider

                for rider in self.riders.values()

                if rider.club.lower() == club_name.lower()

            ],

            key=lambda r: r.cma,

            reverse=True

        )

    # --------------------------------------------------

    def update_statistics(
        self,
        rider_id,
        rides,
        points,
        bonus,
    ):

        rider = self.get_rider(rider_id)

        if rider is None:
            return

        rider.meetings += 1

        rider.rides += rides

        rider.points += points

        rider.bonus_points += bonus

        total = rider.points + rider.bonus_points

        rider.average = (

            total / rider.rides

            if rider.rides

            else 0.0

        )

    # --------------------------------------------------

    def injure_rider(
        self,
        rider_id,
        days,
    ):

        rider = self.get_rider(rider_id)

        if rider:

            rider.injury_days = days

            rider.fitness = 0

    # --------------------------------------------------

    def advance_day(self):

        for rider in self.riders.values():

            if rider.injury_days > 0:

                rider.injury_days -= 1

                if rider.injury_days == 0:

                    rider.fitness = 100

    # --------------------------------------------------

    def export_database(
        self,
        file_path,
    ):

        output = []

        for rider in self.riders.values():

            output.append(rider.__dict__)

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                output,
                f,
                indent=4
            )


rider_database_manager = RiderDatabaseManager()
