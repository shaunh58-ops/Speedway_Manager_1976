"""
British League Speedway Manager

Race Simulation Engine

Version: Alpha 0.1

Simulates Speedway heats and produces results.
"""


from __future__ import annotations


from dataclasses import dataclass


from typing import List


import random



from core.logger import get_logger


from core.event_bus import event_bus



log = get_logger(

    "RaceSimulationEngine"

)



# ==========================================================
# HEAT RESULT
# ==========================================================


@dataclass
class HeatResult:


    rider_id: str


    rider_name: str


    finishing_position: int


    points: int



# ==========================================================
# RACE ENGINE
# ==========================================================


class RaceSimulationEngine:


    def __init__(self):


        self.last_result = []



    # ======================================================
    # SIMULATE HEAT
    ======================================================


    def simulate_heat(
        self,
        riders: List,
        track=None,
        weather=None,
        home_team=None,
    ):


        log.info(

            "Simulating Speedway heat"

        )



        performance = []



        for rider in riders:


            score = self.calculate_performance(

                rider,

                track,

                weather,

                home_team

            )


            performance.append(

                (

                    rider,

                    score

                )

            )



        performance.sort(

            key=lambda x: x[1],

            reverse=True

        )



        results = []



        for position, item in enumerate(

            performance,

            start=1

        ):


            rider = item[0]



            results.append(

                HeatResult(

                    rider_id=rider.rider_id,

                    rider_name=rider.name,

                    finishing_position=position,

                    points=self.points_for_position(

                        position

                    )

                )

            )



        self.last_result = results



        event_bus.publish(

            "heat_completed",

            results=results

        )



        return results



    # ======================================================
    # PERFORMANCE CALCULATION
    ======================================================


    def calculate_performance(
        self,
        rider,
        track,
        weather,
        home_team,
    ):


        score = 0



        # CMA ability

        score += rider.cma * 10



        # Random race variation

        score += random.uniform(

            -15,

            15

        )



        # Home advantage

        if home_team:


            if rider.team == home_team:


                score += 5



        # Track ability

        if track:


            if hasattr(

                rider,

                "track_preferences"

            ):


                if track.name in rider.track_preferences:


                    score += 8



        # Weather impact

        if weather:


            if hasattr(

                rider,

                "weather_skill"

            ):


                score += rider.weather_skill



        return score



    # ======================================================
    # POINTS SYSTEM
    ======================================================


    def points_for_position(
        self,
        position,
    ):


        points = {


            1:3,

            2:2,

            3:1,

            4:0

        }


        return points.get(

            position,

            0

        )



    # ======================================================
    # LAST RESULT
    ======================================================


    def get_last_result(self):


        return self.last_result



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


race_simulation_engine = RaceSimulationEngine()



# ==========================================================
# TEST
# ==========================================================


if __name__ == "__main__":


    print(

        "Race Simulation Engine Ready"

    )
