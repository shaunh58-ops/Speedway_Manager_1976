"""
Speedway Game Engine

Fixture Manager Module

Version: 1.0

Controls Speedway fixture schedules.

Features:

- Fixture database import
- Fixture creation
- Calendar management
- Postponements
- Re-arranged meetings
- Fixture tracking

"""


from typing import Dict, List, Optional


from models import Fixture



class FixtureManager:



    def __init__(self):


        self.fixtures: Dict[int, Fixture] = {}


        self.postponed = []


        self.completed = []



    # =========================================================
    # FIXTURE CREATION
    # =========================================================


    def load_fixtures(
            self,
            fixture_data: List[dict]
    ):


        """
        Convert JSON fixture records
        into Fixture objects.
        """


        for data in fixture_data:


            fixture = Fixture(

                id=data.get(
                    "id"
                ),

                season=data.get(
                    "season",
                    1976
                ),

                round_number=data.get(
                    "round",
                    1
                ),

                home_club_id=data.get(
                    "home_club_id"
                ),

                away_club_id=data.get(
                    "away_club_id"
                ),

                venue_id=data.get(
                    "venue_id"
                )

            )


            self.fixtures[fixture.id] = fixture



        return len(
            self.fixtures
        )



    # =========================================================
    # FIXTURE ACCESS
    # =========================================================


    def get_fixture(
            self,
            fixture_id: int
    ) -> Optional[Fixture]:


        return self.fixtures.get(
            fixture_id
        )



    def get_season_fixtures(
            self,
            season: int
    ) -> List[Fixture]:


        return [

            fixture

            for fixture in self.fixtures.values()

            if fixture.season == season

        ]



    def get_round_fixtures(
            self,
            round_number: int
    ) -> List[Fixture]:


        return [

            fixture

            for fixture in self.fixtures.values()

            if fixture.round_number ==
            round_number

        ]



    # =========================================================
    # FIXTURE STATUS
    # =========================================================


    def complete_fixture(
            self,
            fixture_id: int
    ):


        fixture = self.get_fixture(

            fixture_id

        )


        if fixture and fixture.completed:


            self.completed.append(
                fixture
            )


            return True


        return False



    def remaining_fixtures(
            self,
            season=None
    ):


        fixtures = self.fixtures.values()


        if season:


            fixtures = [

                f

                for f in fixtures

                if f.season == season

            ]



        return [

            fixture

            for fixture in fixtures

            if not fixture.completed

        ]



    # =========================================================
    # POSTPONEMENT SYSTEM
    # =========================================================


    def postpone_fixture(
            self,
            fixture_id: int,
            reason="Weather"
    ):


        fixture = self.get_fixture(

            fixture_id

        )


        if not fixture:

            return False



        self.postponed.append(

            {

                "fixture":

                    fixture,

                "reason":

                    reason

            }

        )


        return True



    def rearrange_fixture(
            self,
            fixture_id: int,
            new_round: int
    ):


        fixture = self.get_fixture(

            fixture_id

        )


        if fixture:


            fixture.round_number = new_round


            return True



        return False



    # =========================================================
    # FIXTURE GENERATOR
    # =========================================================


    def generate_league_schedule(
            self,
            clubs: List,
            season: int
    ):


        """
        Creates a simple home and away
        league fixture list.

        """

        fixture_id = (

            max(
                self.fixtures.keys(),
                default=0
            )

            + 1

        )


        round_number = 1



        for home in clubs:


            for away in clubs:


                if home.id != away.id:


                    fixture = Fixture(

                        id=fixture_id,

                        season=season,

                        round_number=round_number,

                        home_club_id=home.id,

                        away_club_id=away.id,

                        venue_id=0

                    )


                    self.fixtures[fixture_id] = fixture


                    fixture_id += 1


                    round_number += 1



        return self.fixtures



    # =========================================================
    # CALENDAR REPORT
    # =========================================================


    def calendar_summary(
            self,
            season
    ):


        fixtures = self.get_season_fixtures(

            season

        )


        return {


            "season":

                season,


            "total":

                len(fixtures),


            "completed":

                len(

                    [

                        f

                        for f in fixtures

                        if f.completed

                    ]

                ),


            "remaining":

                len(

                    [

                        f

                        for f in fixtures

                        if not f.completed

                    ]

                )

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    manager = FixtureManager()


    test_fixture = [

        {

            "id":1,

            "season":1976,

            "round":1,

            "home_club_id":5,

            "away_club_id":8,

            "venue_id":3

        }

    ]


    manager.load_fixtures(
        test_fixture
    )


    print(

        manager.calendar_summary(
            1976
        )

    )
