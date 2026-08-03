"""
Speedway Game Engine
Database Loader Module

Version: 1.0
Purpose:
    Handles loading and accessing all game databases.

Supported Databases:
    - Riders
    - Clubs
    - Fixtures
    - Venues

Designed for:
    Historical Speedway Simulation
    British Speedway 1976 Project
"""


import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class DatabaseLoader:
    """
    Central database management class.
    """

    def __init__(self, database_folder="database"):

        self.database_folder = Path(database_folder)

        self.riders = []
        self.clubs = []
        self.fixtures = []
        self.venues = []

        self.loaded = False


    # ---------------------------------------------------------
    # Internal JSON Loader
    # ---------------------------------------------------------

    def _load_json(self, filename: str) -> List[Dict]:

        file_path = self.database_folder / filename

        if not file_path.exists():
            print(f"WARNING: Database file missing: {file_path}")
            return []


        try:

            with open(file_path, "r", encoding="utf-8") as file:

                data = json.load(file)


            if isinstance(data, list):
                return data


            print(
                f"WARNING: {filename} does not contain a JSON list"
            )

            return []


        except json.JSONDecodeError:

            print(
                f"ERROR: Invalid JSON format in {filename}"
            )

            return []


        except Exception as error:

            print(
                f"ERROR loading {filename}: {error}"
            )

            return []



    # ---------------------------------------------------------
    # Load All Databases
    # ---------------------------------------------------------

    def load_all(self):

        print("Loading Speedway databases...")


        self.riders = self._load_json(
            "riders.json"
        )


        self.clubs = self._load_json(
            "clubs.json"
        )


        self.fixtures = self._load_json(
            "fixtures.json"
        )


        self.venues = self._load_json(
            "venues.json"
        )


        self.loaded = True


        print(
            f"Riders Loaded: {len(self.riders)}"
        )

        print(
            f"Clubs Loaded: {len(self.clubs)}"
        )

        print(
            f"Fixtures Loaded: {len(self.fixtures)}"
        )

        print(
            f"Venues Loaded: {len(self.venues)}"
        )


        return True



    # ---------------------------------------------------------
    # Rider Database Functions
    # ---------------------------------------------------------

    def get_rider_by_id(
            self,
            rider_id: int
    ) -> Optional[Dict]:


        for rider in self.riders:

            if rider.get("id") == rider_id:

                return rider


        return None



    def search_riders(
            self,
            name: str
    ) -> List[Dict]:


        name = name.lower()


        return [

            rider for rider in self.riders

            if name in rider.get(
                "name",
                ""
            ).lower()

        ]



    # ---------------------------------------------------------
    # Club Database Functions
    # ---------------------------------------------------------

    def get_club_by_id(
            self,
            club_id: int
    ) -> Optional[Dict]:


        for club in self.clubs:

            if club.get("id") == club_id:

                return club


        return None



    def get_clubs_by_year(
            self,
            year: int
    ) -> List[Dict]:


        return [

            club for club in self.clubs

            if club.get("year") == year

        ]



    # ---------------------------------------------------------
    # Fixture Database Functions
    # ---------------------------------------------------------

    def get_fixtures_by_year(
            self,
            year: int
    ) -> List[Dict]:


        return [

            fixture for fixture in self.fixtures

            if fixture.get("year") == year

        ]



    def get_fixture_round(
            self,
            round_number: int
    ) -> List[Dict]:


        return [

            fixture for fixture in self.fixtures

            if fixture.get(
                "round"
            ) == round_number

        ]



    # ---------------------------------------------------------
    # Database Status
    # ---------------------------------------------------------

    def database_summary(self):

        return {

            "riders":
                len(self.riders),

            "clubs":
                len(self.clubs),

            "fixtures":
                len(self.fixtures),

            "venues":
                len(self.venues)

        }



# -------------------------------------------------------------
# Simple Test Runner
# -------------------------------------------------------------

if __name__ == "__main__":


    database = DatabaseLoader()


    database.load_all()


    print(
        database.database_summary()
    )
