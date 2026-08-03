"""
Speedway Game Engine

Stadium Manager Module

Version: 1.0

Controls stadium development, facilities,
attendance and revenue generation.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class Stadium:


    id: int

    name: str

    club_id: int

    capacity: int

    track_quality: int = 70

    facilities: int = 50

    reputation: int = 50

    maintenance_level: int = 70

    age: int = 0

    upgrades: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class StadiumManager:


    def __init__(self):

        self.stadiums: Dict[int, Stadium] = {}

        self.history = []



    # ======================================================
    # CREATION
    # ======================================================


    def create_stadium(
            self,
            stadium_id,
            name,
            club_id,
            capacity
    ):


        stadium = Stadium(

            id=stadium_id,

            name=name,

            club_id=club_id,

            capacity=capacity

        )


        self.stadiums[stadium_id] = stadium


        return stadium



    # ======================================================
    # RETRIEVAL
    # ======================================================


    def get_stadium(
            self,
            stadium_id
    ):


        return self.stadiums.get(

            stadium_id

        )



    # ======================================================
    # ATTENDANCE
    # ======================================================


    def calculate_attendance(
            self,
            stadium,
            club_form,
            opponent_strength
    ):


        base = stadium.capacity * 0.45


        form_bonus = (

            club_form *

            stadium.capacity *

            0.005

        )


        opponent_bonus = (

            opponent_strength *

            stadium.capacity *

            0.003

        )


        reputation_bonus = (

            stadium.reputation *

            stadium.capacity *

            0.002

        )


        attendance = (

            base

            +

            form_bonus

            +

            opponent_bonus

            +

            reputation_bonus

        )


        return min(

            int(attendance),

            stadium.capacity

        )



    # ======================================================
    # REVENUE
    # ======================================================


    def calculate_matchday_income(
            self,
            stadium,
            attendance
    ):


        ticket_price = 5


        facility_bonus = (

            stadium.facilities /

            100

        )


        return int(

            attendance *

            ticket_price *

            (

                1 +

                facility_bonus

            )

        )



    # ======================================================
    # UPGRADES
    # ======================================================


    def upgrade_stadium(
            self,
            stadium_id,
            upgrade_type
    ):


        stadium = self.get_stadium(

            stadium_id

        )


        if not stadium:

            return False



        if upgrade_type == "capacity":


            stadium.capacity += 1000



        elif upgrade_type == "facilities":


            stadium.facilities += 10



        elif upgrade_type == "track":


            stadium.track_quality += 10



        elif upgrade_type == "reputation":


            stadium.reputation += 5



        else:

            return False



        stadium.upgrades.append(

            upgrade_type

        )


        self.history.append({

            "stadium":

                stadium.name,

            "upgrade":

                upgrade_type

        })


        return True



    # ======================================================
    # MAINTENANCE
    # ======================================================


    def annual_maintenance(
            self,
            stadium
    ):


        stadium.age += 1


        if stadium.maintenance_level > 0:

            stadium.maintenance_level -= 5



        if stadium.maintenance_level < 30:

            stadium.track_quality -= 5



    # ======================================================
    # VENUE EFFECT
    # ======================================================


    def home_advantage(
            self,
            stadium
    ):


        advantage = (

            stadium.track_quality *

            0.05

        )


        advantage += (

            stadium.reputation *

            0.03

        )


        return round(

            advantage,

            2

        )



    # ======================================================
    # REPORT
    # ======================================================


    def stadium_report(
            self,
            stadium_id
    ):


        stadium = self.get_stadium(

            stadium_id

        )


        if not stadium:

            return None



        return {


            "name":

                stadium.name,


            "capacity":

                stadium.capacity,


            "track":

                stadium.track_quality,


            "facilities":

                stadium.facilities,


            "reputation":

                stadium.reputation,


            "age":

                stadium.age

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = StadiumManager()


    stadium = manager.create_stadium(

        1,

        "Hyde Road",

        10,

        40000

    )


    print(

        manager.stadium_report(1)

    )
