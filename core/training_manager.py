"""
Speedway Game Engine

Training Manager Module

Version: 1.0

Controls rider development and decline.

Features:

- Rider training
- Youth development
- CMA growth
- Experience gains
- Fitness management
- Career progression

"""


import random


from typing import List



class TrainingManager:



    def __init__(self):


        self.training_history = {}



    # =========================================================
    # RIDER TRAINING
    # =========================================================


    def train_rider(
            self,
            rider,
            intensity="normal"
    ):


        improvement = 0



        if intensity == "light":


            improvement = random.uniform(

                0.01,

                0.05

            )



        elif intensity == "heavy":


            improvement = random.uniform(

                0.10,

                0.30

            )



        else:


            improvement = random.uniform(

                0.05,

                0.15

            )



        # Young riders improve quicker


        if rider.age < 23:


            improvement *= 1.5



        # Experienced riders improve slowly


        if rider.age > 32:


            improvement *= 0.5



        old_cma = rider.current_cma



        rider.current_cma += improvement



        # Respect rider potential


        if rider.current_cma > rider.potential:


            rider.current_cma = rider.potential



        rider.experience += 1



        self.record_training(

            rider,

            old_cma,

            rider.current_cma

        )



        return round(

            rider.current_cma - old_cma,

            2

        )



    # =========================================================
    # TEAM TRAINING
    # =========================================================


    def train_team(
            self,
            club
    ):


        results = []



        for rider in club.squad:


            improvement = self.train_rider(

                rider

            )


            results.append(

                {


                "rider":

                    rider.name,


                "improvement":

                    improvement

                }

            )



        return results



    # =========================================================
    # FITNESS MANAGEMENT
    # =========================================================


    def update_fitness(
            self,
            rider
    ):


        if not hasattr(

            rider,

            "fitness"

        ):


            rider.fitness = 100



        change = random.randint(

            -5,

            5

        )



        rider.fitness += change



        rider.fitness = max(

            0,

            min(

                100,

                rider.fitness

            )

        )



        return rider.fitness



    # =========================================================
    # AGE RELATED DECLINE
    # =========================================================


    def apply_age_decline(
            self,
            rider
    ):


        decline = 0



        if rider.age >= 35:


            decline = random.uniform(

                0.05,

                0.20

            )



        if rider.age >= 40:


            decline = random.uniform(

                0.20,

                0.50

            )



        rider.current_cma -= decline



        rider.current_cma = max(

            0,

            rider.current_cma

        )



        return round(

            decline,

            2

        )



    # =========================================================
    # EXPERIENCE SYSTEM
    # =========================================================


    def gain_experience(
            self,
            rider,
            meetings
    ):


        gained = meetings / 10



        rider.experience += gained



        return round(

            gained,

            2

        )



    # =========================================================
    # TRAINING HISTORY
    # =========================================================


    def record_training(
            self,
            rider,
            before,
            after
    ):


        if rider.id not in self.training_history:


            self.training_history[rider.id] = []



        self.training_history[rider.id].append(

            {


            "before":

                round(before,2),


            "after":

                round(after,2),


            "improvement":

                round(

                    after-before,

                    2

                )

            }

        )



    def rider_development_report(
            self,
            rider
    ):


        return {


            "rider":

                rider.name,


            "age":

                rider.age,


            "current_cma":

                round(

                    rider.current_cma,

                    2

                ),


            "potential":

                rider.potential,


            "experience":

                rider.experience,


            "training_history":

                self.training_history.get(

                    rider.id,

                    []

                )

        }



    # =========================================================
    # SEASON DEVELOPMENT
    # =========================================================


    def end_of_season_update(
            self,
            riders: List
    ):


        results = []



        for rider in riders:


            rider.age += 1



            self.apply_age_decline(

                rider

            )


            self.update_fitness(

                rider

            )


            results.append(

                self.rider_development_report(

                    rider

                )

            )



        return results



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    print(

        "Training Manager Loaded"

    )
