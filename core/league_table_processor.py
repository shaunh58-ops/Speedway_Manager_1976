"""
British League Speedway Manager

League Table Processor

Version: Alpha 0.1

Maintains competition standings.
"""


from __future__ import annotations


from dataclasses import dataclass, field


from typing import Dict, List



from core.logger import get_logger


from core.event_bus import event_bus



log = get_logger(

    "LeagueTableProcessor"

)



# ==========================================================
# CLUB STANDING
# ==========================================================


@dataclass
class ClubStanding:


    club_name: str


    meetings: int = 0


    wins: int = 0


    draws: int = 0


    losses: int = 0


    match_points_for: int = 0


    match_points_against: int = 0


    league_points: int = 0



    @property
    def difference(self):


        return (

            self.match_points_for

            -

            self.match_points_against

        )



# ==========================================================
# LEAGUE TABLE PROCESSOR
# ==========================================================


class LeagueTableProcessor:


    def __init__(self):


        self.table: Dict[str, ClubStanding] = {}



    # ======================================================
    # REGISTER CLUB
    # ======================================================


    def register_club(
        self,
        club_name,
    ):


        if club_name not in self.table:


            self.table[club_name] = ClubStanding(

                club_name=club_name

            )


            log.info(

                f"Registered club: {club_name}"

            )



    # ======================================================
    # REGISTER CLUB LIST
    # ======================================================


    def initialise(
        self,
        clubs,
    ):


        for club in clubs:


            self.register_club(

                club.name

            )



    # ======================================================
    # PROCESS MEETING RESULT
    ======================================================


    def process_result(
        self,
        result,
    ):


        home = self.table.get(

            result.home_team

        )


        away = self.table.get(

            result.away_team

        )



        if not home or not away:


            raise ValueError(

                "Unknown club in result"

            )



        home.meetings += 1


        away.meetings += 1



        home.match_points_for += result.home_points


        home.match_points_against += result.away_points



        away.match_points_for += result.away_points


        away.match_points_against += result.home_points



        # Determine result


        if result.home_points > result.away_points:


            home.wins += 1


            away.losses += 1


            home.league_points += 2



        elif result.away_points > result.home_points:


            away.wins += 1


            home.losses += 1


            away.league_points += 2



        else:


            home.draws += 1


            away.draws += 1


            home.league_points += 1


            away.league_points += 1



        event_bus.publish(

            "league_updated",

            table=self.get_table()

        )



        log.info(

            "League table updated"

        )



    # ======================================================
    # SORT TABLE
    ======================================================


    def get_table(self):


        return sorted(

            self.table.values(),

            key=lambda club: (

                club.league_points,

                club.difference,

                club.match_points_for

            ),

            reverse=True

        )



    # ======================================================
    # POSITION LOOKUP
    ======================================================


    def get_position(
        self,
        club_name,
    ):


        standings = self.get_table()



        for position, club in enumerate(

            standings,

            start=1

        ):


            if club.club_name == club_name:


                return position



        return None



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


league_table_processor = LeagueTableProcessor()
