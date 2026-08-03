"""
Speedway Game Engine

Rider Skill Manager Module

Version: 1.0

Controls detailed rider abilities,
attributes and progression.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class RiderSkills:


    rider_id: int

    starting: int

    cornering: int

    overtaking: int

    track_craft: int

    race_intelligence: int

    fitness: int

    machinery_setup: int

    wet_track: int

    pressure: int

    consistency: int

    history: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class RiderSkillManager:


    def __init__(self):

        self.skills: Dict[int, RiderSkills] = {}



    # ======================================================
    # CREATE RIDER PROFILE
    # ======================================================


    def create_profile(
            self,
            rider_id,
            base_rating
    ):


        def generate():

            variation = random.randint(

                -10,

                10

            )

            return max(

                1,

                min(

                    100,

                    base_rating + variation

                )

            )



        profile = RiderSkills(

            rider_id=rider_id,

            starting=generate(),

            cornering=generate(),

            overtaking=generate(),

            track_craft=generate(),

            race_intelligence=generate(),

            fitness=generate(),

            machinery_setup=generate(),

            wet_track=generate(),

            pressure=generate(),

            consistency=generate()

        )


        self.skills[rider_id] = profile


        return profile



    # ======================================================
    # OVERALL RATING
    # ======================================================


    def overall_rating(
            self,
            rider_id
    ):


        rider = self.skills[rider_id]


        values = [

            rider.starting,

            rider.cornering,

            rider.overtaking,

            rider.track_craft,

            rider.race_intelligence,

            rider.fitness,

            rider.machinery_setup,

            rider.wet_track,

            rider.pressure,

            rider.consistency

        ]


        return round(

            sum(values) / len(values),

            1

        )



    # ======================================================
    # RACE MODIFIER
    # ======================================================


    def race_modifier(
            self,
            rider_id,
            conditions="dry"
    ):


        rider = self.skills[rider_id]


        modifier = 0



        modifier += (

            rider.starting - 50

        ) / 20



        modifier += (

            rider.race_intelligence - 50

        ) / 25



        if conditions == "wet":


            modifier += (

                rider.wet_track - 50

            ) / 10



        if conditions == "high_pressure":


            modifier += (

                rider.pressure - 50

            ) / 15



        return round(

            modifier,

            2

        )



    # ======================================================
    # TRAIN SKILL
    # ======================================================


    def improve_skill(
            self,
            rider_id,
            skill,
            amount
    ):


        rider = self.skills[rider_id]


        if hasattr(

            rider,

            skill

        ):


            current = getattr(

                rider,

                skill

            )


            setattr(

                rider,

                skill,

                min(

                    100,

                    current + amount

                )

            )


            rider.history.append(

                f"{skill} improved by {amount}"

            )



    # ======================================================
    # RANDOM DEVELOPMENT
    # ======================================================


    def seasonal_development(
            self,
            rider_id
    ):


        rider = self.skills[rider_id]


        skill_list = [

            "starting",

            "cornering",

            "overtaking",

            "track_craft",

            "fitness"

        ]


        chosen = random.choice(

            skill_list

        )


        self.improve_skill(

            rider_id,

            chosen,

            1

        )


        return chosen



    # ======================================================
    # STRENGTH ANALYSIS
    # ======================================================


    def strengths(
            self,
            rider_id
    ):


        rider = self.skills[rider_id]


        attributes = vars(rider)


        return sorted(

            [

                (

                    key,

                    value

                )

                for key,value

                in attributes.items()

                if isinstance(

                    value,

                    int

                )

            ],

            key=lambda x:x[1],

            reverse=True

        )[:3]



    # ======================================================
    # WEAKNESSES
    # ======================================================


    def weaknesses(
            self,
            rider_id
    ):


        rider = self.skills[rider_id]


        attributes = vars(rider)


        return sorted(

            [

                (

                    key,

                    value

                )

                for key,value

                in attributes.items()

                if isinstance(

                    value,

                    int

                )

            ],

            key=lambda x:x[1]

        )[:3]



    # ======================================================
    # REPORT
    # ======================================================


    def skill_report(
            self,
            rider_id
    ):


        rider = self.skills[rider_id]


        return {


            "overall":

                self.overall_rating(

                    rider_id

                ),


            "strengths":

                self.strengths(

                    rider_id

                ),


            "weaknesses":

                self.weaknesses(

                    rider_id

                )

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = RiderSkillManager()


    manager.create_profile(

        1,

        75

    )


    print(

        manager.skill_report(

            1

        )

    )
