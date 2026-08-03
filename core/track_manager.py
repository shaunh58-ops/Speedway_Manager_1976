"""
Speedway Game Engine

Track Manager Module

Version: 1.0

Controls Speedway venues,
track characteristics and rider advantages.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class TrackProfile:


    venue_id: int

    name: str

    location: str

    length_meters: int

    capacity: int

    track_type: str

    difficulty: int

    overtaking_rating: int

    home_advantage: int

    preparation_style: str

    notes: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class TrackManager:


    def __init__(self):

        self.tracks: Dict[int, TrackProfile] = {}



    # ======================================================
    # CREATE TRACK
    # ======================================================


    def create_track(
            self,
            venue_id,
            name,
            location,
            length,
            capacity,
            track_type
    ):


        track = TrackProfile(

            venue_id=venue_id,

            name=name,

            location=location,

            length_meters=length,

            capacity=capacity,

            track_type=track_type,

            difficulty=50,

            overtaking_rating=50,

            home_advantage=10,

            preparation_style="Standard"

        )


        self.tracks[venue_id] = track


        return track



    # ======================================================
    # UPDATE CHARACTERISTICS
    # ======================================================


    def update_characteristics(
            self,
            venue_id,
            difficulty=None,
            overtaking=None,
            home_advantage=None,
            preparation=None
    ):


        track = self.tracks[venue_id]


        if difficulty is not None:

            track.difficulty = difficulty



        if overtaking is not None:

            track.overtaking_rating = overtaking



        if home_advantage is not None:

            track.home_advantage = home_advantage



        if preparation is not None:

            track.preparation_style = preparation



        return track



    # ======================================================
    # RACE MODIFIER
    # ======================================================


    def race_modifier(
            self,
            venue_id,
            rider
    ):


        track = self.tracks[venue_id]


        modifier = 0



        if track.track_type == "Technical":


            modifier += (

                rider.track_craft - 50

            ) / 10



            modifier += (

                rider.race_intelligence - 50

            ) / 15



        elif track.track_type == "Fast":


            modifier += (

                rider.starting - 50

            ) / 10



            modifier += (

                rider.machinery_setup - 50

            ) / 15



        elif track.track_type == "Heavy":


            modifier += (

                rider.fitness - 50

            ) / 10



        return round(

            modifier,

            2

        )



    # ======================================================
    # HOME ADVANTAGE
    # ======================================================


    def home_bonus(
            self,
            venue_id
    ):


        track = self.tracks[venue_id]


        return track.home_advantage / 10



    # ======================================================
    # OVERTAKING CHANCE
    # ======================================================


    def overtaking_chance(
            self,
            venue_id
    ):


        track = self.tracks[venue_id]


        return track.overtaking_rating



    # ======================================================
    # SEARCH
    # ======================================================


    def find_track(
            self,
            name
    ):


        for track in self.tracks.values():


            if track.name.lower() == name.lower():

                return track



        return None



    # ======================================================
    # REPORT
    ======================================================


    def track_report(
            self,
            venue_id
    ):


        track = self.tracks.get(

            venue_id

        )


        if not track:

            return None



        return {


            "name":

                track.name,


            "length":

                track.length_meters,


            "type":

                track.track_type,


            "difficulty":

                track.difficulty,


            "overtaking":

                track.overtaking_rating

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = TrackManager()


    manager.create_track(

        1,

        "Belle Vue",

        "Manchester",

        285,

        40000,

        "Technical"

    )


    print(

        manager.track_report(

            1

        )

    )
