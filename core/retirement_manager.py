"""
Speedway Game Engine

Retirement Manager Module

Version: 1.0

Controls rider retirement and career endings.

Features:

- Retirement decisions
- Career evaluation
- Hall of Fame
- Farewell records
- Post career status

"""


import random


from typing import Dict, List



class RetirementManager:



    def __init__(self):


        self.retired_riders: Dict[int, dict] = {}



        self.hall_of_fame = []



    # =========================================================
    # RETIREMENT CALCULATION
    # =========================================================


    def retirement_probability(
            self,
            rider
    ):


        probability = 0



        # Age factor


        if rider.age >= 38:


            probability += 20



        if rider.age >= 42:


            probability += 35



        if rider.age >= 45:


            probability += 50



        # Performance decline


        if rider.current_cma < 6:


            probability += 25



        if rider.current_cma < 4:


            probability += 40



        # Injury history


        if hasattr(

            rider,

            "injuries"

        ):


            if rider.injuries > 20:


                probability += 20



        # Successful riders often continue longer


        if hasattr(

            rider,

            "championships"

        ):


            if rider.championships > 0:


                probability -= 15



        return max(

            0,

            min(

                probability,

                95

            )

        )



    # =========================================================
    # RETIREMENT DECISION
    # =========================================================


    def should_retire(
            self,
            rider
    ):


        chance = self.retirement_probability(

            rider

        )


        roll = random.randint(

            1,

            100

        )


        return roll <= chance



    # =========================================================
    # PROCESS RIDER RETIREMENT
    # =========================================================


    def retire_rider(
            self,
            rider,
            reason="Career Decision"
    ):


        rider.retired = True



        record = {


            "rider_id":

                rider.id,


            "name":

                rider.name,


            "age":

                rider.age,


            "final_cma":

                round(

                    rider.current_cma,

                    2

                ),


            "reason":

                reason,


            "career_achievements":

                getattr(

                    rider,

                    "championships",

                    0

                )

        }



        self.retired_riders[rider.id] = record



        self.evaluate_hall_of_fame(

            rider,

            record

        )



        return record



    # =========================================================
    # END OF SEASON CHECK
    # =========================================================


    def process_season(
            self,
            riders: List
    ):


        retirements = []



        for rider in riders:


            if not rider.retired:


                if self.should_retire(

                    rider

                ):


                    retirements.append(

                        self.retire_rider(

                            rider

                        )

                    )



        return retirements



    # =========================================================
    # HALL OF FAME
    # =========================================================


    def evaluate_hall_of_fame(
            self,
            rider,
            record
    ):


        score = 0



        score += (

            rider.current_cma *

            5

        )



        score += (

            getattr(

                rider,

                "championships",

                0

            )

            *

            25

        )



        score += (

            getattr(

                rider,

                "career_wins",

                0

            )

            *

            0.5

        )



        if score >= 100:


            self.hall_of_fame.append(

                record

            )


            return True



        return False



    # =========================================================
    # CAREER SUMMARY
    # =========================================================


    def career_summary(
            self,
            rider_id
    ):


        return self.retired_riders.get(

            rider_id,

            None

        )



    # =========================================================
    # HALL OF FAME REPORT
    # =========================================================


    def hall_of_fame_list(self):


        return self.hall_of_fame



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    retirement = RetirementManager()


    print(

        "Retirement Manager Loaded"

    )
