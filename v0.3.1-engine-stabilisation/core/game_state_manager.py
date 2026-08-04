"""
Speedway Game Engine

Game State Manager Module

Version: 1.0

Controls the active world state
of the Speedway universe.

"""


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List
from datetime import date



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class CareerState:


    manager_name: str = ""

    club_id: int | None = None

    reputation: int = 50

    career_years: int = 0



@dataclass(slots=True)
class ChampionshipState:


    current_competition: str = ""

    champion: str = ""

    standings: Dict = field(
        default_factory=dict
    )



@dataclass(slots=True)
class GameState:


    game_year: int = 1976

    current_date: str = field(

        default_factory=lambda:

        str(date.today())

    )


    season_active: bool = False


    career: CareerState = field(

        default_factory=CareerState

    )


    championship: ChampionshipState = field(

        default_factory=ChampionshipState

    )


    riders: Dict = field(

        default_factory=dict

    )


    teams: Dict = field(

        default_factory=dict

    )


    venues: Dict = field(

        default_factory=dict

    )


    records: List = field(

        default_factory=list

    )


    historical_events: List = field(

        default_factory=list

    )



# ==========================================================
# MANAGER
# ==========================================================


class GameStateManager:


    def __init__(self):

        self.state = GameState()



    # ======================================================
    # START NEW GAME
    # ======================================================


    def create_new_game(
            self,
            year,
            manager_name,
            club_id
    ):


        self.state = GameState()


        self.state.game_year = year


        self.state.career.manager_name = manager_name


        self.state.career.club_id = club_id


        self.state.season_active = True



        return self.state



    # ======================================================
    # DATE MANAGEMENT
    # ======================================================


    def update_date(
            self,
            new_date
    ):


        self.state.current_date = new_date



    # ======================================================
    # RIDERS
    ======================================================


    def add_rider(
            self,
            rider_id,
            rider_data
    ):


        self.state.riders[rider_id] = rider_data



    def remove_rider(
            self,
            rider_id
    ):


        if rider_id in self.state.riders:


            del self.state.riders[rider_id]



    # ======================================================
    # TEAMS
    ======================================================


    def add_team(
            self,
            team_id,
            team_data
    ):


        self.state.teams[team_id] = team_data



    # ======================================================
    # VENUES
    ======================================================


    def add_venue(
            self,
            venue_id,
            venue_data
    ):


        self.state.venues[venue_id] = venue_data



    # ======================================================
    # CHAMPIONSHIP
    ======================================================


    def update_champion(
            self,
            name
    ):


        self.state.championship.champion = name



    def update_standings(
            self,
            standings
    ):


        self.state.championship.standings = standings



    # ======================================================
    # HISTORY
    ======================================================


    def add_historical_event(
            self,
            event
    ):


        self.state.historical_events.append(

            event

        )



    # ======================================================
    # RECORDS
    ======================================================


    def add_record(
            self,
            record
    ):


        self.state.records.append(

            record

        )



    # ======================================================
    # CAREER
    ======================================================


    def progress_career_year(self):


        self.state.career.career_years += 1


        self.state.game_year += 1



    # ======================================================
    # EXPORT STATE
    ======================================================


    def export_state(self):


        return asdict(

            self.state

        )



    # ======================================================
    # IMPORT STATE
    ======================================================


    def import_state(
            self,
            data
    ):


        self.state = GameState(

            **data

        )



    # ======================================================
    # SUMMARY
    ======================================================


    def summary(self):


        return {


            "year":

                self.state.game_year,


            "date":

                self.state.current_date,


            "teams":

                len(

                    self.state.teams

                ),


            "riders":

                len(

                    self.state.riders

                ),


            "champion":

                self.state.championship.champion

        }



# ==========================================================
# GLOBAL STATE
# ==========================================================


game_state = GameStateManager()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    game_state.create_new_game(

        1976,

        "Shaun",

        1

    )


    print(

        game_state.summary()

    )
