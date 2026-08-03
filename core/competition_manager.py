"""
Speedway Game Engine

Competition Manager Module

Version: 1.0

Controls Speedway competitions,
standings and championships.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class CompetitionRules:


    points_for_win: int = 3

    points_for_draw: int = 1

    points_for_loss: int = 0

    heats_per_meeting: int = 15



@dataclass(slots=True)
class Competition:


    competition_id: int

    name: str

    competition_type: str

    year: int

    rules: CompetitionRules

    entrants: List = field(

        default_factory=list

    )

    standings: Dict = field(

        default_factory=dict

    )

    results: List = field(

        default_factory=list

    )

    champion: Optional[str] = None



# ==========================================================
# COMPETITION MANAGER
# ==========================================================


class CompetitionManager:


    def __init__(self):


        self.competitions: Dict[int, Competition] = {}

        self.next_id = 1



    # ======================================================
    # CREATE COMPETITION
    # ======================================================


    def create_competition(
            self,
            name,
            competition_type,
            year,
            rules=None
    ):


        if rules is None:

            rules = CompetitionRules()



        competition = Competition(

            self.next_id,

            name,

            competition_type,

            year,

            rules

        )


        self.competitions[self.next_id] = competition


        self.next_id += 1



        return competition



    # ======================================================
    # ADD ENTRANT
    # ======================================================


    def add_entrant(
            self,
            competition_id,
            entrant
    ):


        competition = self.get_competition(

            competition_id

        )


        if competition:


            competition.entrants.append(

                entrant

            )


            competition.standings[entrant] = 0



    # ======================================================
    # RECORD RESULT
    # ======================================================


    def record_result(
            self,
            competition_id,
            winner,
            loser=None
    ):


        competition = self.get_competition(

            competition_id

        )


        if not competition:

            return False



        result = {


            "winner": winner,

            "loser": loser

        }



        competition.results.append(

            result

        )


        self.update_points(

            competition,

            winner,

            loser

        )


        return True



    # ======================================================
    # UPDATE POINTS
    # ======================================================


    def update_points(
            self,
            competition,
            winner,
            loser
    ):


        if winner in competition.standings:


            competition.standings[winner] += (

                competition.rules.points_for_win

            )



        if (

            loser

            and

            loser in competition.standings

        ):


            competition.standings[loser] += (

                competition.rules.points_for_loss

            )



    # ======================================================
    # TABLE
    # ======================================================


    def get_standings(
            self,
            competition_id
    ):


        competition = self.get_competition(

            competition_id

        )


        if not competition:

            return []



        return sorted(

            competition.standings.items(),

            key=lambda x: x[1],

            reverse=True

        )



    # ======================================================
    # DECLARE CHAMPION
    # ======================================================


    def calculate_champion(
            self,
            competition_id
    ):


        standings = self.get_standings(

            competition_id

        )


        if standings:


            champion = standings[0][0]


            self.competitions[competition_id].champion = champion


            return champion



        return None



    # ======================================================
    # GET COMPETITION
    # ======================================================


    def get_competition(
            self,
            competition_id
    ):


        return self.competitions.get(

            competition_id

        )



    # ======================================================
    # LIST COMPETITIONS
    ======================================================


    def list_competitions(self):


        return list(

            self.competitions.values()

        )



    # ======================================================
    # REPORT
    ======================================================


    def report(self):


        return [

            {

                "name": competition.name,

                "type": competition.competition_type,

                "year": competition.year,

                "champion": competition.champion

            }

            for competition

            in self.competitions.values()

        ]



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


competition_manager = CompetitionManager()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    league = competition_manager.create_competition(

        "British League",

        "LEAGUE",

        1976

    )


    competition_manager.add_entrant(

        league.competition_id,

        "Belle Vue"

    )


    competition_manager.add_entrant(

        league.competition_id,

        "Wolverhampton"

    )


    competition_manager.record_result(

        league.competition_id,

        "Belle Vue",

        "Wolverhampton"

    )


    print(

        competition_manager.get_standings(

            league.competition_id

        )

    )
