"""
Speedway Game Engine

Season Manager Module

Version: 1.0

Controls complete Speedway seasons.

Features:

- Fixture management
- League progression
- Match simulation
- League table
- Season completion
- End of year processing

"""


from typing import List, Dict


from models import Fixture


class SeasonManager:



    def __init__(
            self,
            year: int,
            race_engine,
            team_manager,
            rider_manager
    ):


        self.year = year

        self.race_engine = race_engine

        self.team_manager = team_manager

        self.rider_manager = rider_manager


        self.fixtures: List[Fixture] = []


        self.completed_fixtures = []


        self.current_round = 1



    # =========================================================
    # FIXTURE MANAGEMENT
    # =========================================================


    def load_fixtures(
            self,
            fixtures: List[Fixture]
    ):


        self.fixtures = fixtures


        return len(
            self.fixtures
        )



    def get_next_fixture(self):


        for fixture in self.fixtures:


            if not fixture.completed:

                return fixture



        return None



    # =========================================================
    # RUN SINGLE MATCH
    # =========================================================


    def run_fixture(
            self,
            fixture: Fixture,
            venues
    ):


        home_team = self.team_manager.get_club(

            fixture.home_club_id

        )


        away_team = self.team_manager.get_club(

            fixture.away_club_id

        )


        venue = venues.get(

            fixture.venue_id

        )



        if not home_team or not away_team:

            return None



        result = self.race_engine.simulate_meeting(

            home_team,

            away_team,

            venue

        )



        fixture.set_result(

            result["home_score"],

            result["away_score"]

        )



        self.update_league_table(

            fixture

        )


        self.completed_fixtures.append(

            fixture

        )


        return result



    # =========================================================
    # LEAGUE TABLE UPDATE
    # =========================================================


    def update_league_table(
            self,
            fixture: Fixture
    ):


        home = self.team_manager.get_club(

            fixture.home_club_id

        )


        away = self.team_manager.get_club(

            fixture.away_club_id

        )


        if fixture.home_score > fixture.away_score:


            home.record_win()

            away.record_loss()



        elif fixture.away_score > fixture.home_score:


            away.record_win()

            home.record_loss()



        else:


            home.points += 1

            away.points += 1



    # =========================================================
    # RUN ROUND
    # =========================================================


    def run_round(
            self,
            venues
    ):


        round_results = []



        for fixture in self.fixtures:


            if (

                fixture.round_number ==
                self.current_round

            ):


                result = self.run_fixture(

                    fixture,

                    venues

                )


                round_results.append(

                    result

                )



        self.current_round += 1


        return round_results



    # =========================================================
    # SEASON SIMULATION
    # =========================================================


    def run_full_season(
            self,
            venues
    ):


        results = []



        while True:


            fixture = self.get_next_fixture()



            if not fixture:

                break



            result = self.run_fixture(

                fixture,

                venues

            )


            results.append(

                result

            )



        return results



    # =========================================================
    # TABLE FUNCTIONS
    # =========================================================


    def league_table(self):


        return self.team_manager.league_table()



    def display_table(self):


        table = []



        for position, club in enumerate(

                self.league_table(),

                start=1

        ):


            table.append(

                {

                "position":
                    position,

                "team":
                    club.name,

                "points":
                    club.points,

                "wins":
                    club.wins,

                "losses":
                    club.defeats

                }

            )



        return table



    # =========================================================
    # SEASON END
    # =========================================================


    def complete_season(self):


        retired = self.rider_manager.check_retirements()



        self.rider_manager.progress_year()



        champion = None



        table = self.league_table()



        if table:

            champion = table[0]



        return {


            "season":
                self.year,


            "champion":
                champion.name
                if champion
                else None,


            "retired_riders":

                len(retired)

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    print(
        "Season Manager Loaded"
    )
