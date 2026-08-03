"""
Speedway Game Engine

Season Calendar Manager Module

Version: 1.0

Controls the structure and phases
of a Speedway season.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


from calendar_engine import CalendarEngine



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class SeasonPhase:


    name: str

    start_date: str

    end_date: str

    activities: List[str] = field(

        default_factory=list

    )



@dataclass(slots=True)
class SeasonRules:


    league_name: str = "British League"

    start_month: int = 4

    end_month: int = 9

    cup_enabled: bool = True

    playoffs_enabled: bool = False

    transfer_window_enabled: bool = True



# ==========================================================
# SEASON CALENDAR MANAGER
# ==========================================================


class SeasonCalendarManager:


    def __init__(
            self,
            calendar_engine: CalendarEngine
    ):


        self.calendar = calendar_engine


        self.rules = SeasonRules()


        self.phases: List[SeasonPhase] = []



        self.current_year = None



    # ======================================================
    # CREATE SEASON
    # ======================================================


    def create_season(
            self,
            year
    ):


        self.current_year = year


        self.calendar.create_season(

            year

        )


        self.create_default_phases()



    # ======================================================
    # DEFAULT SEASON PHASES
    # ======================================================


    def create_default_phases(self):


        year = self.current_year


        self.phases = [


            SeasonPhase(

                "Winter Preparation",

                f"{year}-01-01",

                f"{year}-02-28",

                [

                    "Transfers",

                    "Equipment Preparation",

                    "Rider Development"

                ]

            ),



            SeasonPhase(

                "Pre Season",

                f"{year}-03-01",

                f"{year}-03-31",

                [

                    "Practice Meetings",

                    "Team Preparation"

                ]

            ),



            SeasonPhase(

                "Competitive Season",

                f"{year}-04-01",

                f"{year}-09-30",

                [

                    "League Fixtures",

                    "Cup Meetings",

                    "International Events"

                ]

            ),



            SeasonPhase(

                "Season Review",

                f"{year}-10-01",

                f"{year}-10-31",

                [

                    "Awards",

                    "Statistics Review"

                ]

            ),



            SeasonPhase(

                "Off Season",

                f"{year}-11-01",

                f"{year}-12-31",

                [

                    "Contracts",

                    "Planning"

                ]

            )

        ]



    # ======================================================
    # ADD LEAGUE FIXTURE PERIOD
    # ======================================================


    def setup_league_calendar(
            self,
            fixtures
    ):


        for fixture in fixtures:


            self.calendar.add_fixture(

                fixture["date"],

                fixture["home_team"],

                fixture["away_team"]

            )



    # ======================================================
    # ADD CUP COMPETITION
    # ======================================================


    def setup_cup_calendar(
            self,
            cup_events
    ):


        if not self.rules.cup_enabled:

            return



        for event in cup_events:


            self.calendar.add_cup_round(

                event["date"],

                event["competition"],

                event["teams"]

            )



    # ======================================================
    # GET CURRENT PHASE
    # ======================================================


    def get_phase(
            self,
            current_date
    ):


        for phase in self.phases:


            if (

                phase.start_date

                <=

                current_date

                <=

                phase.end_date

            ):

                return phase



        return None



    # ======================================================
    # TRANSFER WINDOW CHECK
    # ======================================================


    def transfer_window_open(
            self,
            current_date
    ):


        if not self.rules.transfer_window_enabled:

            return False



        phase = self.get_phase(

            current_date

        )


        if not phase:

            return False



        return phase.name in [

            "Winter Preparation",

            "Off Season"

        ]



    # ======================================================
    # SEASON COMPLETE
    # ======================================================


    def season_complete(
            self
    ):


        return (

            self.current_year is not None

            and

            len(

                self.calendar.calendar.events

            )

            >

            0

        )



    # ======================================================
    # REPORT
    # ======================================================


    def report(self):


        return {


            "year":

            self.current_year,


            "league":

            self.rules.league_name,


            "phases":

            [

                phase.name

                for phase

                in self.phases

            ],


            "events":

            len(

                self.calendar.calendar.events

            )

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    engine = CalendarEngine()


    manager = SeasonCalendarManager(

        engine

    )


    manager.create_season(

        1976

    )


    print(

        manager.report()

    )
