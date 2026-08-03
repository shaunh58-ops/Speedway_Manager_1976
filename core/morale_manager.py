"""
Speedway Game Engine

Morale Manager Module

Version: 1.0

Controls rider confidence, team morale
and psychological performance effects.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class RiderMorale:


    rider_id: int

    confidence: int = 50

    happiness: int = 50

    motivation: int = 50

    pressure: int = 20

    form_momentum: int = 0

    events: List[str] = field(
        default_factory=list
    )



@dataclass(slots=True)
class TeamMorale:


    club_id: int

    atmosphere: int = 50

    unity: int = 50

    winning_streak: int = 0

    losing_streak: int = 0

    events: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class MoraleManager:


    def __init__(self):

        self.riders: Dict[int, RiderMorale] = {}

        self.teams: Dict[int, TeamMorale] = {}



    # ======================================================
    # PROFILE CREATION
    # ======================================================


    def get_rider_morale(
            self,
            rider_id
    ):


        if rider_id not in self.riders:


            self.riders[rider_id] = RiderMorale(

                rider_id=rider_id

            )


        return self.riders[rider_id]



    def get_team_morale(
            self,
            club_id
    ):


        if club_id not in self.teams:


            self.teams[club_id] = TeamMorale(

                club_id=club_id

            )


        return self.teams[club_id]



    # ======================================================
    # PERFORMANCE EVENTS
    # ======================================================


    def record_result(
            self,
            rider_id,
            result
    ):


        morale = self.get_rider_morale(

            rider_id

        )


        if result == "win":


            morale.confidence += 8

            morale.motivation += 5

            morale.form_momentum += 2



        elif result == "podium":


            morale.confidence += 4



        elif result == "poor":


            morale.confidence -= 5

            morale.pressure += 5



        morale.events.append(

            result

        )


        self.clamp(

            morale

        )



    # ======================================================
    # TEAM RESULTS
    # ======================================================


    def record_team_result(
            self,
            club_id,
            result
    ):


        team = self.get_team_morale(

            club_id

        )


        if result == "win":


            team.winning_streak += 1

            team.losing_streak = 0

            team.atmosphere += 5

            team.unity += 3



        else:


            team.losing_streak += 1

            team.winning_streak = 0

            team.atmosphere -= 4



        team.events.append(

            result

        )


        self.clamp_team(

            team

        )



    # ======================================================
    # EXTERNAL PRESSURE
    # ======================================================


    def apply_pressure(
            self,
            rider_id,
            amount
    ):


        morale = self.get_rider_morale(

            rider_id

        )


        morale.pressure += amount


        morale.confidence -= (

            amount //

            2

        )


        self.clamp(

            morale

        )



    # ======================================================
    # TEAM SUPPORT
    # ======================================================


    def team_support_bonus(
            self,
            rider_id,
            club_id
    ):


        rider = self.get_rider_morale(

            rider_id

        )


        team = self.get_team_morale(

            club_id

        )


        return round(

            (

                rider.confidence

                +

                team.atmosphere

                +

                team.unity

            )

            /

            30,

            2

        )



    # ======================================================
    # PERFORMANCE MODIFIER
    ======================================================


    def performance_modifier(
            self,
            rider_id
    ):


        morale = self.get_rider_morale(

            rider_id

        )


        modifier = (

            morale.confidence

            +

            morale.motivation

            +

            morale.form_momentum

            -

            morale.pressure

        )


        return round(

            modifier /

            100,

            2

        )



    # ======================================================
    # SEASON UPDATE
    # ======================================================


    def season_reset(
            self
    ):


        for morale in self.riders.values():


            morale.pressure = max(

                0,

                morale.pressure - 10

            )


            morale.form_momentum = 0



    # ======================================================
    # CONTROL
    ======================================================


    def clamp(
            self,
            morale
    ):


        values = [

            "confidence",

            "happiness",

            "motivation",

            "pressure"

        ]


        for value in values:


            current = getattr(

                morale,

                value

            )


            setattr(

                morale,

                value,

                max(

                    0,

                    min(

                        100,

                        current

                    )

                )

            )



    def clamp_team(
            self,
            team
    ):


        team.atmosphere = max(

            0,

            min(

                100,

                team.atmosphere

            )

        )


        team.unity = max(

            0,

            min(

                100,

                team.unity

            )

        )



    # ======================================================
    # REPORT
    # ======================================================


    def rider_report(
            self,
            rider_id
    ):


        morale = self.get_rider_morale(

            rider_id

        )


        return {


            "confidence":

                morale.confidence,


            "happiness":

                morale.happiness,


            "motivation":

                morale.motivation,


            "pressure":

                morale.pressure

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = MoraleManager()


    manager.record_result(

        1,

        "win"

    )


    print(

        manager.rider_report(1)

    )
