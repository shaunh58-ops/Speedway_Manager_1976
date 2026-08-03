"""
Speedway Game Engine

Race Engine Module

Version: 1.0

Simulates Speedway races and meetings.

Features:

- Heat simulation
- Rider performance calculation
- CMA influence
- Form effects
- Home advantage
- Mechanical failures
- Heat scoring

"""


import random

from typing import List, Dict


from models import (
    Rider,
    Venue
)



class RaceEngine:



    def __init__(self):

        self.race_history = []



    # =========================================================
    # RIDER PERFORMANCE CALCULATION
    # =========================================================


    def calculate_rider_power(
            self,
            rider: Rider,
            venue: Venue = None,
            home_rider=False
    ):


        if rider.retired:

            return 0



        power = rider.current_cma



        # Current form

        power *= rider.form



        # Experience bonus

        if rider.age >= 30:

            power *= 1.03



        # Young rider inconsistency

        if rider.age < 21:

            power *= random.uniform(
                0.90,
                1.10
            )



        # Home track advantage

        if venue and home_rider:

            power *= venue.home_advantage



        # Random Speedway variation

        power *= random.uniform(
            0.85,
            1.15
        )


        return round(
            power,
            2
        )



    # =========================================================
    # MECHANICAL FAILURE
    # =========================================================


    def mechanical_failure(
            self,
            rider: Rider
    ):


        risk = 5


        # Older riders have more risk

        if rider.age > 35:

            risk += 5



        roll = random.randint(
            1,
            100
        )


        return roll <= risk



    # =========================================================
    # SINGLE HEAT SIMULATION
    # =========================================================


    def simulate_heat(
            self,
            home_riders: List[Rider],
            away_riders: List[Rider],
            venue: Venue = None
    ):



        competitors = []



        for rider in home_riders:


            power = self.calculate_rider_power(

                rider,

                venue,

                True

            )


            competitors.append(

                {

                    "rider":
                        rider,

                    "team":
                        "home",

                    "power":
                        power

                }

            )



        for rider in away_riders:


            power = self.calculate_rider_power(

                rider,

                venue,

                False

            )


            competitors.append(

                {

                    "rider":
                        rider,

                    "team":
                        "away",

                    "power":
                        power

                }

            )



        # Remove mechanical failures


        finishers = []



        for competitor in competitors:


            if not self.mechanical_failure(

                competitor["rider"]

            ):


                finishers.append(
                    competitor
                )



        # Sort by performance


        finishers.sort(

            key=lambda x:
                x["power"],

            reverse=True

        )



        results = []



        for position, rider in enumerate(

                finishers,

                start=1

        ):


            results.append(

                {

                "position":
                    position,

                "rider":
                    rider["rider"].name,

                "team":
                    rider["team"]

                }

            )



        return results



    # =========================================================
    # HEAT SCORING
    # =========================================================


    def calculate_heat_points(
            self,
            results: List[Dict]
    ):


        points = {


            "home":
                0,


            "away":
                0

        }



        scoring = [

            3,
            2,
            1,
            0

        ]



        for index, result in enumerate(results):


            if index < len(scoring):


                points[result["team"]] += scoring[index]



        return points



    # =========================================================
    # FULL MEETING SIMULATION
    # =========================================================


    def simulate_meeting(
            self,
            home_team,
            away_team,
            venue: Venue,
            heats=15
    ):


        meeting = {


            "home":
                home_team.name,


            "away":
                away_team.name,


            "heats":[],

            "home_score":
                0,

            "away_score":
                0

        }



        home_lineup = home_team.squad[:]

        away_lineup = away_team.squad[:]



        for heat_number in range(

                1,

                heats + 1

        ):


            home_selection = [

                home_lineup[
                    heat_number %
                    len(home_lineup)
                ]

            ]



            away_selection = [

                away_lineup[
                    heat_number %
                    len(away_lineup)
                ]

            ]



            result = self.simulate_heat(

                home_selection,

                away_selection,

                venue

            )



            points = self.calculate_heat_points(

                result

            )



            meeting["home_score"] += points["home"]

            meeting["away_score"] += points["away"]



            meeting["heats"].append(

                {

                "heat":
                    heat_number,

                "results":
                    result,

                "points":
                    points

                }

            )



        self.race_history.append(
            meeting
        )


        return meeting



    # =========================================================
    # REPORTING
    # =========================================================


    def last_result(self):

        if self.race_history:

            return self.race_history[-1]


        return None



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    from models import Club, Venue



    rider1 = Rider(

        1,

        "Legend Rider",

        current_cma=10.5

    )


    rider2 = Rider(

        2,

        "Young Rider",

        current_cma=7.2

    )



    home = Club(

        1,

        "Example Wolves",

        "England",

        1928

    )


    away = Club(

        2,

        "Example Tigers",

        "England",

        1930

    )



    home.add_rider(
        rider1
    )

    away.add_rider(
        rider2
    )



    track = Venue(

        1,

        "Example Stadium",

        "England",

        300,

        10000,

        home_advantage=1.05

    )



    engine = RaceEngine()



    result = engine.simulate_meeting(

        home,

        away,

        track

    )


    print(result)
