"""
Speedway Game Engine

Championship Manager Module

Version: 1.0

Controls individual rider championships,
qualifying systems and championship records.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class ChampionshipRules:


    points_win: int = 3

    points_second: int = 2

    points_third: int = 1

    riders_qualified: int = 16



@dataclass(slots=True)
class RiderStanding:


    rider_name: str

    points: int = 0

    meetings: int = 0

    wins: int = 0



@dataclass(slots=True)
class Championship:


    name: str

    year: int

    championship_type: str

    rules: ChampionshipRules

    riders: Dict[str, RiderStanding] = field(

        default_factory=dict

    )

    champion: Optional[str] = None

    history: List = field(

        default_factory=list

    )



# ==========================================================
# CHAMPIONSHIP MANAGER
# ==========================================================


class ChampionshipManager:


    def __init__(self):

        self.championships: Dict[str, Championship] = {}



    # ======================================================
    # CREATE CHAMPIONSHIP
    # ======================================================


    def create_championship(
            self,
            name,
            year,
            championship_type,
            rules=None
    ):


        if rules is None:

            rules = ChampionshipRules()



        championship = Championship(

            name,

            year,

            championship_type,

            rules

        )


        self.championships[name] = championship


        return championship



    # ======================================================
    # REGISTER RIDER
    # ======================================================


    def register_rider(
            self,
            championship_name,
            rider_name
    ):


        championship = self.get_championship(

            championship_name

        )


        if championship:


            championship.riders[rider_name] = RiderStanding(

                rider_name

            )



    # ======================================================
    # RECORD RESULT
    # ======================================================


    def record_result(
            self,
            championship_name,
            rider_name,
            finishing_position
    ):


        championship = self.get_championship(

            championship_name

        )


        if not championship:

            return False



        rider = championship.riders.get(

            rider_name

        )


        if not rider:

            return False



        rider.meetings += 1



        if finishing_position == 1:


            rider.points += championship.rules.points_win

            rider.wins += 1



        elif finishing_position == 2:


            rider.points += championship.rules.points_second



        elif finishing_position == 3:


            rider.points += championship.rules.points_third



        return True



    # ======================================================
    # STANDINGS
    # ======================================================


    def standings(
            self,
            championship_name
    ):


        championship = self.get_championship(

            championship_name

        )


        if not championship:

            return []



        return sorted(

            championship.riders.values(),

            key=lambda rider:

                rider.points,

            reverse=True

        )



    # ======================================================
    # DECLARE CHAMPION
    # ======================================================


    def calculate_champion(
            self,
            championship_name
    ):


        table = self.standings(

            championship_name

        )


        if table:


            champion = table[0].rider_name


            championship = self.get_championship(

                championship_name

            )


            championship.champion = champion



            championship.history.append(

                {

                    "year":

                    championship.year,


                    "winner":

                    champion

                }

            )


            return champion



        return None



    # ======================================================
    # QUALIFICATION
    # ======================================================


    def qualified_riders(
            self,
            championship_name
    ):


        championship = self.get_championship(

            championship_name

        )


        if not championship:

            return []



        riders = self.standings(

            championship_name

        )


        return riders[

            :championship.rules.riders_qualified

        ]



    # ======================================================
    # LOOKUP
    # ======================================================


    def get_championship(
            self,
            name
    ):


        return self.championships.get(

            name

        )



    # ======================================================
    # HISTORY
    ======================================================


    def championship_history(
            self,
            name
    ):


        championship = self.get_championship(

            name

        )


        if championship:

            return championship.history



        return []



    # ======================================================
    # REPORT
    # ======================================================


    def report(self):


        return [

            {

                "name":

                championship.name,


                "year":

                championship.year,


                "champion":

                championship.champion

            }

            for championship

            in self.championships.values()

        ]



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


championship_manager = ChampionshipManager()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    championship_manager.create_championship(

        "World Championship",

        1976,

        "WORLD"

    )


    championship_manager.register_rider(

        "World Championship",

        "Peter Collins"

    )


    championship_manager.register_rider(

        "World Championship",

        "Ole Olsen"

    )


    championship_manager.record_result(

        "World Championship",

        "Peter Collins",

        1

    )


    championship_manager.record_result(

        "World Championship",

        "Ole Olsen",

        2

    )


    print(

        championship_manager.standings(

            "World Championship"

        )

    )
