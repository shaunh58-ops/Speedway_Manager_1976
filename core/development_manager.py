"""
Speedway Game Engine

Development Manager Module

Version: 1.0

Controls rider improvement,
potential and long-term progression.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class RiderDevelopment:


    rider_id: int

    age: int

    ability: int

    potential: int

    work_ethic: int

    experience: int = 0

    training_bonus: int = 0

    coach_bonus: int = 0

    development_history: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class DevelopmentManager:


    def __init__(self):

        self.riders: Dict[int, RiderDevelopment] = {}



    # ======================================================
    # CREATE PROFILE
    # ======================================================


    def create_profile(
            self,
            rider_id,
            age,
            ability,
            potential=None
    ):


        if potential is None:

            potential = random.randint(

                ability,

                95

            )


        profile = RiderDevelopment(

            rider_id=rider_id,

            age=age,

            ability=ability,

            potential=potential,

            work_ethic=random.randint(

                40,

                95

            )

        )


        self.riders[rider_id] = profile


        return profile



    # ======================================================
    # TRAINING INPUT
    # ======================================================


    def apply_training(
            self,
            rider_id,
            intensity
    ):


        rider = self.riders[rider_id]


        rider.training_bonus += intensity


        rider.training_bonus = min(

            20,

            rider.training_bonus

        )



    # ======================================================
    # COACHING INPUT
    # ======================================================


    def apply_coaching(
            self,
            rider_id,
            coach_quality
    ):


        rider = self.riders[rider_id]


        rider.coach_bonus += coach_quality // 10


        rider.coach_bonus = min(

            20,

            rider.coach_bonus

        )



    # ======================================================
    # SEASON DEVELOPMENT
    ======================================================


    def process_season(
            self,
            rider_id
    ):


        rider = self.riders[rider_id]


        growth = 0



        # Young riders improve faster

        if rider.age < 23:

            growth += 2



        elif rider.age < 30:

            growth += 1



        else:

            growth -= 1



        growth += (

            rider.work_ethic //

            30

        )


        growth += (

            rider.training_bonus //

            5

        )


        growth += (

            rider.coach_bonus //

            5

        )



        growth += random.randint(

            -1,

            2

        )



        if rider.ability < rider.potential:


            rider.ability += growth



            rider.ability = min(

                rider.ability,

                rider.potential

            )


            rider.development_history.append(

                f"Improved by {growth} points"

            )



        else:


            rider.development_history.append(

                "Reached maximum potential"

            )



        rider.experience += 1

        rider.age += 1


        self.reset_bonuses(

            rider

        )


        return rider.ability



    # ======================================================
    # AGE DECLINE
    ======================================================


    def apply_decline(
            self,
            rider_id
    ):


        rider = self.riders[rider_id]


        if rider.age >= 35:


            decline = random.randint(

                0,

                2

            )


            rider.ability -= decline



            rider.ability = max(

                1,

                rider.ability

            )


            rider.development_history.append(

                "Career decline applied"

            )



    # ======================================================
    # POTENTIAL CHECK
    ======================================================


    def reached_peak(
            self,
            rider_id
    ):


        rider = self.riders[rider_id]


        return rider.ability >= rider.potential



    # ======================================================
    # RESET
    ======================================================


    def reset_bonuses(
            self,
            rider
    ):


        rider.training_bonus = 0

        rider.coach_bonus = 0



    # ======================================================
    # REPORT
    ======================================================


    def development_report(
            self,
            rider_id
    ):


        rider = self.riders.get(

            rider_id

        )


        if not rider:

            return None



        return {


            "age":

                rider.age,


            "ability":

                rider.ability,


            "potential":

                rider.potential,


            "experience":

                rider.experience,


            "history":

                rider.development_history[-5:]

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = DevelopmentManager()


    rider = manager.create_profile(

        1,

        18,

        55,

        90

    )


    manager.apply_training(

        1,

        10

    )


    manager.process_season(

        1

    )


    print(

        manager.development_report(

            1

        )

    )
