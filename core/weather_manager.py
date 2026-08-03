"""
Speedway Game Engine

Weather Manager Module

Version: 1.0

Controls weather conditions and their impact
on Speedway meetings.

"""


from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Dict


class WeatherType(str, Enum):

    SUNNY = "Sunny"

    CLOUDY = "Cloudy"

    OVERCAST = "Overcast"

    LIGHT_RAIN = "Light Rain"

    HEAVY_RAIN = "Heavy Rain"

    STORM = "Storm"



@dataclass(slots=True)
class WeatherCondition:


    weather: WeatherType

    temperature: int

    wind_speed: int

    humidity: int

    track_moisture: int

    postponement_risk: int



class WeatherManager:


    def __init__(self):

        self.history = []



    # ======================================================
    # WEATHER GENERATION
    # ======================================================


    def generate_weather(
            self,
            month: int,
            region: str
    ) -> WeatherCondition:


        temperature = self.generate_temperature(

            month

        )


        weather = self.generate_condition(

            month,

            region

        )


        wind = random.randint(

            0,

            40

        )


        humidity = random.randint(

            30,

            95

        )


        moisture = self.calculate_track_moisture(

            weather,

            humidity

        )


        postponement = self.calculate_postponement(

            weather

        )


        condition = WeatherCondition(

            weather=weather,

            temperature=temperature,

            wind_speed=wind,

            humidity=humidity,

            track_moisture=moisture,

            postponement_risk=postponement

        )


        self.history.append(condition)


        return condition



    # ======================================================
    # WEATHER TYPES
    # ======================================================


    def generate_condition(
            self,
            month,
            region
    ):


        rain_chance = 25


        if region in (

            "England",

            "Scotland",

            "Wales"

        ):

            rain_chance += 15



        if month in (

            11,

            12,

            1,

            2

        ):

            rain_chance += 20



        roll = random.randint(

            1,

            100

        )


        if roll <= 5:

            return WeatherType.STORM


        if roll <= rain_chance:

            return WeatherType.LIGHT_RAIN


        if roll <= rain_chance + 5:

            return WeatherType.HEAVY_RAIN


        if roll <= 70:

            return WeatherType.CLOUDY


        if roll <= 90:

            return WeatherType.OVERCAST


        return WeatherType.SUNNY



    # ======================================================
    # TEMPERATURE
    # ======================================================


    def generate_temperature(
            self,
            month
    ):


        averages = {

            1: 5,

            2: 6,

            3: 9,

            4: 12,

            5: 16,

            6: 19,

            7: 21,

            8: 21,

            9: 17,

            10: 13,

            11: 9,

            12: 6

        }


        base = averages.get(

            month,

            15

        )


        return base + random.randint(

            -5,

            5

        )



    # ======================================================
    # TRACK CONDITIONS
    # ======================================================


    def calculate_track_moisture(
            self,
            weather,
            humidity
    ):


        moisture = humidity // 3


        if weather == WeatherType.LIGHT_RAIN:

            moisture += 20


        elif weather == WeatherType.HEAVY_RAIN:

            moisture += 40


        elif weather == WeatherType.STORM:

            moisture += 60



        return min(

            moisture,

            100

        )



    # ======================================================
    # POSTPONEMENTS
    # ======================================================


    def calculate_postponement(
            self,
            weather
    ):


        risks = {

            WeatherType.SUNNY: 0,

            WeatherType.CLOUDY: 0,

            WeatherType.OVERCAST: 5,

            WeatherType.LIGHT_RAIN: 15,

            WeatherType.HEAVY_RAIN: 70,

            WeatherType.STORM: 95

        }


        return risks[weather]



    # ======================================================
    # RACING EFFECTS
    # ======================================================


    def rider_modifier(
            self,
            rider,
            condition
    ):


        modifier = 0


        moisture = condition.track_moisture



        if moisture > 60:

            modifier += getattr(

                rider,

                "wet_track_skill",

                0

            )



        if condition.wind_speed > 25:

            modifier += getattr(

                rider,

                "experience",

                0

            ) / 20



        return round(

            modifier,

            2

        )



    # ======================================================
    # REPORT
    # ======================================================


    def weather_report(
            self,
            condition
    ):


        return {

            "conditions":

                condition.weather.value,

            "temperature":

                condition.temperature,

            "wind":

                condition.wind_speed,

            "track_moisture":

                condition.track_moisture,

            "postponement":

                condition.postponement_risk

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = WeatherManager()


    weather = manager.generate_weather(

        7,

        "England"

    )


    print(

        manager.weather_report(weather)

    )
