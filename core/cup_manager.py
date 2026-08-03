"""
Speedway Game Engine

Cup Manager Module

Version: 1.0

Controls knockout competitions,
cup rounds and tournament progression.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class CupTeam:


    club_id: int

    name: str

    eliminated: bool = False



@dataclass(slots=True)
class CupTie:


    home_team: int

    away_team: int

    home_score: int = 0

    away_score: int = 0

    completed: bool = False



@dataclass(slots=True)
class CupCompetition:


    id: int

    name: str

    season: int

    teams: Dict[int, CupTeam] = field(
        default_factory=dict
    )

    rounds: Dict[str, List[CupTie]] = field(
        default_factory=dict
    )

    winner: int | None = None



# ==========================================================
# MANAGER
# ==========================================================


class CupManager:


    def __init__(self):

        self.competitions: Dict[int, CupCompetition] = {}



    # ======================================================
    # CREATE COMPETITION
    # ======================================================


    def create_cup(
            self,
            cup_id,
            name,
            season
    ):


        cup = CupCompetition(

            id=cup_id,

            name=name,

            season=season

        )


        self.competitions[cup_id] = cup


        return cup



    # ======================================================
    # ADD TEAMS
    # ======================================================


    def add_team(
            self,
            cup_id,
            club_id,
            name
    ):


        cup = self.competitions[cup_id]


        cup.teams[club_id] = CupTeam(

            club_id=club_id,

            name=name

        )



    # ======================================================
    # CREATE DRAW
    # ======================================================


    def create_draw(
            self,
            cup_id,
            round_name
    ):


        cup = self.competitions[cup_id]


        teams = list(

            cup.teams.values()

        )


        random.shuffle(

            teams

        )


        ties = []


        for index in range(

            0,

            len(teams),

            2

        ):


            if index + 1 < len(teams):


                ties.append(

                    CupTie(

                        home_team=

                        teams[index].club_id,


                        away_team=

                        teams[index + 1].club_id

                    )

                )


        cup.rounds[round_name] = ties


        return ties



    # ======================================================
    # RECORD TIE RESULT
    # ======================================================


    def record_result(
            self,
            cup_id,
            round_name,
            tie_index,
            home_score,
            away_score
    ):


        cup = self.competitions[cup_id]


        tie = cup.rounds[round_name][

            tie_index

        ]


        tie.home_score = home_score

        tie.away_score = away_score

        tie.completed = True



    # ======================================================
    # DETERMINE WINNER
    # ======================================================


    def determine_winners(
            self,
            cup_id,
            round_name
    ):


        cup = self.competitions[cup_id]


        winners = []


        for tie in cup.rounds[round_name]:


            if tie.home_score > tie.away_score:


                winners.append(

                    tie.home_team

                )


            elif tie.away_score > tie.home_score:


                winners.append(

                    tie.away_team

                )


            else:


                winners.append(

                    random.choice(

                        [

                            tie.home_team,

                            tie.away_team

                        ]

                    )

                )


        return winners



    # ======================================================
    # ADVANCE ROUND
    # ======================================================


    def create_next_round(
            self,
            cup_id,
            previous_round,
            next_round
    ):


        winners = self.determine_winners(

            cup_id,

            previous_round

        )


        random.shuffle(

            winners

        )


        cup = self.competitions[cup_id]


        ties = []


        for index in range(

            0,

            len(winners),

            2

        ):


            if index + 1 < len(winners):


                ties.append(

                    CupTie(

                        winners[index],

                        winners[index + 1]

                    )

                )


        cup.rounds[next_round] = ties


        return ties



    # ======================================================
    # FINAL
    # ======================================================


    def declare_winner(
            self,
            cup_id,
            finalist_a,
            finalist_b,
            score_a,
            score_b
    ):


        cup = self.competitions[cup_id]


        if score_a > score_b:


            cup.winner = finalist_a


        else:


            cup.winner = finalist_b



        return cup.winner



    # ======================================================
    # REPORT
    # ======================================================


    def cup_report(
            self,
            cup_id
    ):


        cup = self.competitions[cup_id]


        return {


            "competition":

                cup.name,


            "season":

                cup.season,


            "winner":

                cup.winner,


            "rounds":

                list(

                    cup.rounds.keys()

                )

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = CupManager()


    manager.create_cup(

        1,

        "British Knockout Cup",

        1976

    )


    manager.add_team(

        1,

        10,

        "Belle Vue"

    )


    manager.add_team(

        1,

        20,

        "Coventry"

    )


    manager.create_draw(

        1,

        "Quarter Final"

    )


    print(

        manager.cup_report(1)

    )
