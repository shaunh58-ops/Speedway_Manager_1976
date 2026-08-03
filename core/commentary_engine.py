"""
Speedway Game Engine

Commentary Engine Module

Version: 1.0

Creates race narratives,
incidents and dramatic moments.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class CommentaryEvent:


    lap: int

    event_type: str

    description: str



@dataclass(slots=True)
class RaceCommentary:


    heat_number: int

    events: List[CommentaryEvent] = field(
        default_factory=list
    )



# ==========================================================
# ENGINE
# ==========================================================


class CommentaryEngine:


    def __init__(self):

        self.history: List[RaceCommentary] = []



    # ======================================================
    # START COMMENTARY
    # ======================================================


    def generate_start(
            self,
            rider_name,
            starting_rating
    ):


        if starting_rating >= 85:


            return CommentaryEvent(

                0,

                "Start",

                f"{rider_name} reacts brilliantly from the tapes and storms into the lead."

            )



        elif starting_rating >= 65:


            return CommentaryEvent(

                0,

                "Start",

                f"{rider_name} makes a solid start and battles into the first bend."

            )



        else:


            return CommentaryEvent(

                0,

                "Start",

                f"{rider_name} struggles away from the gate and has work to do."

            )



    # ======================================================
    # OVERTAKE COMMENTARY
    # ======================================================


    def generate_overtake(
            self,
            attacker,
            defender
    ):


        styles = [

            f"{attacker} dives underneath {defender} with a brave inside move.",

            f"{attacker} sweeps around the outside and takes the position.",

            f"{attacker} applies pressure and forces {defender} into a mistake."

        ]


        return CommentaryEvent(

            2,

            "Overtake",

            random.choice(

                styles

            )

        )



    # ======================================================
    # FINAL LAP
    ======================================================


    def generate_final_lap(
            self,
            rider,
            winning
    ):


        if winning:


            text = (

                f"{rider} holds his nerve on the final lap "
                "and charges towards victory."

            )


        else:


            text = (

                f"{rider} fights desperately on the final lap "
                "but cannot find a way through."

            )


        return CommentaryEvent(

            4,

            "Final Lap",

            text

        )



    # ======================================================
    # INCIDENTS
    # ======================================================


    def generate_incident(
            self,
            rider
    ):


        incident = random.choice(

            [

                f"{rider} loses control briefly but stays upright.",

                f"{rider} suffers a mechanical problem and slows dramatically.",

                f"{rider} clips the dirt but continues the race."

            ]

        )


        return CommentaryEvent(

            2,

            "Incident",

            incident

        )



    # ======================================================
    # WEATHER COMMENTARY
    ======================================================


    def weather_commentary(
            self,
            weather
    ):


        if weather.track_condition == "Heavy":


            return CommentaryEvent(

                0,

                "Weather",

                "The track is heavy after rain and rewards the most skilful riders."

            )



        if weather.wind_strength > 7:


            return CommentaryEvent(

                0,

                "Weather",

                "Strong winds make bike control difficult around the circuit."

            )



        return CommentaryEvent(

            0,

            "Weather",

            "Conditions are perfect for an exciting Speedway meeting."

        )



    # ======================================================
    # CREATE HEAT COMMENTARY
    ======================================================


    def create_heat_commentary(
            self,
            heat_number
    ):


        commentary = RaceCommentary(

            heat_number

        )


        self.history.append(

            commentary

        )


        return commentary



    # ======================================================
    # ADD EVENT
    ======================================================


    def add_event(
            self,
            commentary,
            event
    ):


        commentary.events.append(

            event

        )



    # ======================================================
    # SUMMARY
    ======================================================


    def heat_summary(
            self,
            commentary
    ):


        return [

            event.description

            for event

            in commentary.events

        ]



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    engine = CommentaryEngine()


    heat = engine.create_heat_commentary(

        1

    )


    engine.add_event(

        heat,

        engine.generate_start(

            "John Smith",

            90

        )

    )


    for line in engine.heat_summary(

        heat

    ):

        print(line)
