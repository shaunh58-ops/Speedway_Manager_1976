"""
Speedway Game Engine

AI Manager Module

Version: 1.0

Controls computer-controlled Speedway teams.

Features:

- Squad evaluation
- Rider recruitment
- Rider releases
- Youth development
- AI strategy

"""


import random


from typing import List



class AIManager:



    def __init__(
            self,
            team_manager,
            rider_manager
    ):


        self.team_manager = team_manager

        self.rider_manager = rider_manager



    # =========================================================
    # TEAM ANALYSIS
    # =========================================================


    def evaluate_team(
            self,
            club
    ):


        if not club.squad:


            return {


                "strength":0,

                "average_age":0,

                "weakness":"No riders"

            }



        strength = sum(

            rider.current_cma

            for rider in club.squad

        )



        average_age = sum(

            rider.age

            for rider in club.squad

        ) / len(club.squad)



        weakness = "Balanced"



        if strength < 50:

            weakness = "Low team strength"



        elif average_age > 35:

            weakness = "Aging squad"



        return {


            "strength":

                round(
                    strength,
                    2
                ),


            "average_age":

                round(
                    average_age,
                    1
                ),


            "weakness":

                weakness

        }



    # =========================================================
    # TRANSFER MARKET
    # =========================================================


    def find_replacement(
            self,
            club
    ):


        available = [

            rider

            for rider

            in self.rider_manager.riders.values()

            if rider.club_id is None

            and not rider.retired

        ]



        if not available:


            return None



        available.sort(

            key=lambda rider:

            (

                rider.current_cma

                +

                rider.potential

            ),

            reverse=True

        )



        return available[0]



    # =========================================================
    # RELEASE RIDERS
    # =========================================================


    def release_weak_riders(
            self,
            club
    ):


        released = []



        if len(club.squad) <= 7:


            return released



        squad = sorted(

            club.squad,

            key=lambda rider:

            rider.current_cma

        )



        weakest = squad[0]



        if weakest.current_cma < 5:


            club.remove_rider(

                weakest.id

            )


            released.append(

                weakest

            )



        return released



    # =========================================================
    # RECRUITMENT
    # =========================================================


    def recruit_rider(
            self,
            club
    ):


        rider = self.find_replacement(

            club

        )


        if rider:


            club.add_rider(

                rider

            )


            rider.club_id = club.id



            return rider



        return None



    # =========================================================
    # YOUTH DEVELOPMENT
    # =========================================================


    def develop_young_riders(
            self,
            club
    ):


        improvements = []



        for rider in club.squad:


            if rider.age < 23:


                growth = random.uniform(

                    0.05,

                    0.25

                )


                rider.current_cma += growth



                improvements.append(

                    {

                    "rider":

                        rider.name,


                    "improvement":

                        round(
                            growth,
                            2
                        )

                    }

                )



        return improvements



    # =========================================================
    # SEASON AI TURN
    # =========================================================


    def process_club(
            self,
            club
    ):


        report = {


            "club":

                club.name,


            "released":[],

            "signed":[],

            "development":[]

        }



        evaluation = self.evaluate_team(

            club

        )



        # Rebuild ageing teams


        if evaluation["weakness"] == "Aging squad":


            report["released"] = (

                self.release_weak_riders(

                    club

                )

            )



            new_rider = self.recruit_rider(

                club

            )


            if new_rider:


                report["signed"].append(

                    new_rider.name

                )



        report["development"] = (

            self.develop_young_riders(

                club

            )

        )



        return report



    # =========================================================
    # WHOLE LEAGUE AI
    # =========================================================


    def process_all_teams(self):


        results = []



        for club in self.team_manager.clubs.values():


            results.append(

                self.process_club(

                    club

                )

            )



        return results



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    print(

        "AI Manager Loaded"

    )
