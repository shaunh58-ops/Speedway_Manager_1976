"""
Speedway Game Engine

Weather Engine Module

Version: 1.0

Controls race night weather,
track conditions and environmental effects.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class WeatherCondition:


    temperature: int

    rain_probability: int

    wind_strength: int

    visibility: int

    track_condition: str

    weather_type: str

    notes: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class WeatherEngine:


    def __init__(self):

        self.history: Dict[str, WeatherCondition] = {}



    # ======================================================
    # GENERATE WEATHER
    # ======================================================


    def generate_weather(
            self,
            month,
            location="UK"
    ):


        if location == "UK":


            temperature = random.randint(

                8,

                25

            )


            rain = random.randint(

                10,

                70

            )


        else:


            temperature = random.randint(

                15,

                35

            )


            rain = random.randint(

                5,

                40

            )



        wind = random.randint(

            0,

            10

        )


        visibility = random.randint(

            70,

            100

        )


        if rain > 60:


            track = "Heavy"


            weather = "Rain"



        elif rain > 30:


            track = "Damp"


            weather = "Cloudy"



        else:


            track = "Fast"


            weather = "Dry"



        condition = WeatherCondition(

            temperature=temperature,

            rain_probability=rain,

            wind_strength=wind,

            visibility=visibility,

            track_condition=track,

            weather_type=weather

        )


        return condition



    # ======================================================
    # TRACK EFFECT
    # ======================================================


    def track_modifier(
            self,
            condition
    ):


        modifier = 0



        if condition.track_condition == "Fast":

            modifier += 5



        elif condition.track_condition == "Damp":

            modifier += 0



        elif condition.track_condition == "Heavy":

            modifier -= 5



        return modifier



    # ======================================================
    # RIDER WEATHER BONUS
    # ======================================================


    def rider_weather_bonus(
            self,
            rider_skill,
            condition
    ):


        bonus = 0



        if condition.track_condition == "Heavy":


            bonus += (

                rider_skill.wet_track - 50

            ) / 10



        if condition.wind_strength > 7:


            bonus += (

                rider_skill.track_craft - 50

            ) / 15



        return round(

            bonus,

            2

        )



    # ======================================================
    # EQUIPMENT EFFECT
    # ======================================================


    def equipment_modifier(
            self,
            equipment,
            condition
    ):


        modifier = 0



        if condition.track_condition == "Heavy":


            modifier += (

                equipment.setup_quality - 50

            ) / 10



        return round(

            modifier,

            2

        )



    # ======================================================
    # RAIN OFF CHECK
    # ======================================================


    def meeting_postponed(
            self,
            condition
    ):


        if condition.rain_probability >= 90:

            return True


        if condition.visibility < 40:

            return True


        return False



    # ======================================================
    # WEATHER REPORT
    # ======================================================


    def weather_report(
            self,
            condition
    ):


        return {


            "weather":

                condition.weather_type,


            "temperature":

                condition.temperature,


            "rain":

                condition.rain_probability,


            "wind":

                condition.wind_strength,


            "track":

                condition.track_condition

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    engine = WeatherEngine()


    weather = engine.generate_weather(

        7

    )


    print(

        engine.weather_report(

            weather

        )

    )
