"""
British League Speedway Manager

Fixture Database Manager

Version: Alpha 0.1

Handles historical Speedway fixture data.
"""


from __future__ import annotations


import json


from pathlib import Path


from dataclasses import dataclass


from typing import Dict, List, Optional



from core.logger import get_logger



log = get_logger(

    "FixtureDatabaseManager"

)



# ==========================================================
# FIXTURE MODEL
# ==========================================================


@dataclass
class Fixture:


    fixture_id: str


    date: str


    competition: str


    home_team: str


    away_team: str


    venue: str = ""


    completed: bool = False


    home_score: int = 0


    away_score: int = 0



# ==========================================================
# FIXTURE DATABASE MANAGER
# ==========================================================


class FixtureDatabaseManager:


    def __init__(
        self,
        database_path=None,
    ):


        self.database_path = database_path


        self.fixtures: Dict[str, Fixture] = {}



    # ======================================================
    # LOAD DATABASE
    ======================================================


    def load_database(
        self,
        file_path=None,
    ):


        path = Path(

            file_path or self.database_path

        )



        if not path.exists():


            raise FileNotFoundError(

                f"Fixture database missing: {path}"

            )



        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:


            data = json.load(file)



        self.fixtures.clear()



        for record in data:


            fixture = self.create_fixture(

                record

            )



            self.fixtures[fixture.fixture_id] = fixture



        log.info(

            f"Loaded {len(self.fixtures)} fixtures"

        )



        return self.fixtures



    # ======================================================
    # CREATE FIXTURE
    ======================================================


    def create_fixture(
        self,
        data,
    ):


        return Fixture(


            fixture_id=str(

                data.get(

                    "id",

                    data.get(

                        "fixture_id",

                        ""

                    )

                )

            ),



            date=data.get(

                "date",

                ""

            ),



            competition=data.get(

                "competition",

                "British League"

            ),



            home_team=data.get(

                "home_team",

                ""

            ),



            away_team=data.get(

                "away_team",

                ""

            ),



            venue=data.get(

                "venue",

                ""

            )

        )



    # ======================================================
    # FIND FIXTURE
    ======================================================


    def get_fixture(
        self,
        fixture_id,
    ) -> Optional[Fixture]:


        return self.fixtures.get(

            fixture_id

        )



    # ======================================================
    # CLUB FIXTURES
    ======================================================


    def get_club_fixtures(
        self,
        club_name,
    ):


        return [

            fixture

            for fixture

            in self.fixtures.values()

            if fixture.home_team == club_name

            or fixture.away_team == club_name

        ]



    # ======================================================
    # UPCOMING FIXTURES
    ======================================================


    def get_upcoming_fixtures(
        self,
        club_name=None,
    ):


        fixtures = [

            fixture

            for fixture

            in self.fixtures.values()

            if not fixture.completed

        ]



        if club_name:


            fixtures = [

                fixture

                for fixture

                in fixtures

                if fixture.home_team == club_name

                or fixture.away_team == club_name

            ]



        return fixtures



    # ======================================================
    # NEXT FIXTURE
    ======================================================


    def get_next_fixture(
        self,
        club_name,
    ):


        fixtures = self.get_upcoming_fixtures(

            club_name

        )



        if fixtures:


            return fixtures[0]



        return None



    # ======================================================
    # COMPLETE FIXTURE
    ======================================================


    def complete_fixture(
        self,
        fixture_id,
        home_score,
        away_score,
    ):


        fixture = self.get_fixture(

            fixture_id

        )



        if fixture:


            fixture.completed = True


            fixture.home_score = home_score


            fixture.away_score = away_score



            log.info(

                f"Fixture completed: {fixture.home_team} vs {fixture.away_team}"

            )



    # ======================================================
    # SEASON PROGRESS
    ======================================================


    def get_completed_count(self):


        return len(

            [

                fixture

                for fixture

                in self.fixtures.values()

                if fixture.completed

            ]

        )



    def get_total_count(self):


        return len(

            self.fixtures

        )



    # ======================================================
    # EXPORT
    ======================================================


    def export_database(
        self,
        file_path,
    ):


        output = []



        for fixture in self.fixtures.values():


            output.append(

                fixture.__dict__

            )



        with open(

            file_path,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                output,

                file,

                indent=4

            )



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


fixture_database_manager = FixtureDatabaseManager()
