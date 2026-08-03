"""
Speedway Game Engine

League Manager Module

Version: 1.0

Controls league structures,
tables and championship systems.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class LeagueClub:


    club_id: int

    name: str

    points: int = 0

    wins: int = 0

    draws: int = 0

    losses: int = 0

    races_for: int = 0

    races_against: int = 0



@dataclass(slots=True)
class League:


    id: int

    name: str

    division: int

    season: int

    clubs: Dict[int, LeagueClub] = field(
        default_factory=dict
    )



# ==========================================================
# MANAGER
# ==========================================================


class LeagueManager:


    def __init__(self):

        self.leagues: Dict[int, League] = {}



    # ======================================================
    # CREATE LEAGUE
    # ======================================================


    def create_league(
            self,
            league_id,
            name,
            division,
            season
    ):


        league = League(

            id=league_id,

            name=name,

            division=division,

            season=season

        )


        self.leagues[league_id] = league


        return league



    # ======================================================
    # ADD CLUB
    # ======================================================


    def add_club(
            self,
            league_id,
            club_id,
            name
    ):


        league = self.leagues.get(

            league_id

        )


        if not league:

            return False



        league.clubs[club_id] = LeagueClub(

            club_id=club_id,

            name=name

        )


        return True



    # ======================================================
    # RECORD RESULT
    # ======================================================


    def record_result(
            self,
            league_id,
            home_id,
            away_id,
            home_score,
            away_score
    ):


        league = self.leagues[

            league_id

        ]


        home = league.clubs[

            home_id

        ]


        away = league.clubs[

            away_id

        ]



        home.races_for += home_score

        home.races_against += away_score


        away.races_for += away_score

        away.races_against += home_score



        if home_score > away_score:


            home.points += 2

            home.wins += 1

            away.losses += 1



        elif away_score > home_score:


            away.points += 2

            away.wins += 1

            home.losses += 1



        else:


            home.points += 1

            away.points += 1

            home.draws += 1

            away.draws += 1



    # ======================================================
    # TABLE GENERATION
    # ======================================================


    def league_table(
            self,
            league_id
    ):


        league = self.leagues[

            league_id

        ]


        return sorted(

            league.clubs.values(),

            key=lambda club:

            (

                club.points,

                club.races_for - club.races_against

            ),

            reverse=True

        )



    # ======================================================
    # CHAMPION
    # ======================================================


    def champion(
            self,
            league_id
    ):


        table = self.league_table(

            league_id

        )


        if table:

            return table[0]


        return None



    # ======================================================
    # PROMOTION / RELEGATION
    ======================================================


    def promotion_candidates(
            self,
            league_id,
            places=2
    ):


        table = self.league_table(

            league_id

        )


        return table[:places]



    def relegation_candidates(
            self,
            league_id,
            places=2
    ):


        table = self.league_table(

            league_id

        )


        return table[-places:]



    # ======================================================
    # SEASON RESET
    ======================================================


    def reset_season(
            self,
            league_id,
            season
    ):


        league = self.leagues[

            league_id

        ]


        league.season = season


        for club in league.clubs.values():


            club.points = 0

            club.wins = 0

            club.draws = 0

            club.losses = 0

            club.races_for = 0

            club.races_against = 0



    # ======================================================
    # REPORT
    ======================================================


    def league_report(
            self,
            league_id
    ):


        table = self.league_table(

            league_id

        )


        return [


            {


                "club":

                    club.name,


                "points":

                    club.points,


                "wins":

                    club.wins


            }


            for club

            in table

        ]



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = LeagueManager()


    manager.create_league(

        1,

        "British League Division One",

        1,

        1976

    )


    manager.add_club(

        1,

        10,

        "Belle Vue"

    )


    manager.add_club(

        1,

        20,

        "Coventry"

    )


    manager.record_result(

        1,

        10,

        20,

        50,

        28

    )


    print(

        manager.league_report(1)

    )
