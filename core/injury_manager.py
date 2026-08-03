"""
Speedway Game Engine

Injury Manager Module

Version: 1.0

Controls rider injuries and recovery.

Features:

- Injury generation
- Recovery tracking
- Rider availability
- Career impact
- Injury history

"""


import random


from typing import Dict, List



class InjuryManager:



    def __init__(self):


        self.injury_history: Dict[int, list] = {}



    # =========================================================
    # INJURY DATABASE
    # =========================================================


    def generate_injury(
            self,
            risk_level="normal"
    ):


        injuries = {


            "Minor": {


                "weeks":

                    random.randint(
                        1,
                        2
                    ),


                "cma_loss":

                    0.05

            },


            "Moderate": {


                "weeks":

                    random.randint(
                        3,
                        6
                    ),


                "cma_loss":

                    0.15

            },


            "Serious": {


                "weeks":

                    random.randint(
                        8,
                        20
                    ),


                "cma_loss":

                    0.35

            },


            "Career Threatening": {


                "weeks":

                    random.randint(
                        30,
                        52
                    ),


                "cma_loss":

                    0.75

            }

        }



        probability = random.random()



        if risk_level == "high":

            probability += 0.15



        if probability < 0.55:


            severity = "Minor"



        elif probability < 0.80:


            severity = "Moderate"



        elif probability < 0.95:


            severity = "Serious"



        else:


            severity = "Career Threatening"



        injury = injuries[severity]



        return {


            "severity":

                severity,


            "weeks":

                injury["weeks"],


            "cma_loss":

                injury["cma_loss"]

        }



    # =========================================================
    # APPLY INJURY
    # =========================================================


    def injure_rider(
            self,
            rider,
            cause="Race Accident"
    ):


        injury = self.generate_injury()



        rider.injuries = injury["weeks"]



        rider.available = False



        original_cma = rider.current_cma



        rider.current_cma = max(

            0,

            rider.current_cma -

            injury["cma_loss"]

        )



        record = {


            "season":

                getattr(
                    rider,
                    "season",
                    None
                ),


            "cause":

                cause,


            "severity":

                injury["severity"],


            "weeks_out":

                injury["weeks"],


            "cma_before":

                original_cma,


            "cma_after":

                rider.current_cma

        }



        if rider.id not in self.injury_history:


            self.injury_history[rider.id] = []



        self.injury_history[rider.id].append(

            record

        )



        return record



    # =========================================================
    # RECOVERY SYSTEM
    # =========================================================


    def process_week(
            self,
            riders: List
    ):


        recovered = []



        for rider in riders:


            if rider.injuries > 0:


                rider.injuries -= 1



                if rider.injuries == 0:


                    rider.available = True



                    recovered.append(

                        rider.name

                    )



        return recovered



    # =========================================================
    # AVAILABILITY
    # =========================================================


    def is_available(
            self,
            rider
    ):


        return (

            rider.injuries == 0

            and

            not rider.retired

        )



    # =========================================================
    # INJURY HISTORY
    # =========================================================


    def rider_injury_history(
            self,
            rider_id
    ):


        return self.injury_history.get(

            rider_id,

            []

        )



    # =========================================================
    # CAREER IMPACT
    # =========================================================


    def career_risk(
            self,
            rider
    ):


        history = self.rider_injury_history(

            rider.id

        )


        serious = 0



        for injury in history:


            if injury["severity"] in [

                "Serious",

                "Career Threatening"

            ]:


                serious += 1



        return {


            "major_injuries":

                serious,


            "career_warning":

                serious >= 3

        }



    # =========================================================
    # REPORT
    # =========================================================


    def injury_report(
            self,
            rider
    ):


        return {


            "rider":

                rider.name,


            "available":

                self.is_available(

                    rider

                ),


            "weeks_remaining":

                rider.injuries,


            "history":

                self.rider_injury_history(

                    rider.id

                )

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    print(

        "Injury Manager Loaded"

    )
