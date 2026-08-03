"""
Speedway Game Engine

Venue Manager Module

Version: 1.0

Controls Speedway venues and track characteristics.

Features:

- Venue database loading
- Track profiles
- Home advantage
- Weather effects
- Track suitability
- Attendance calculation

"""


import random

from typing import Dict, List, Optional


from models import Venue



class VenueManager:



    def __init__(self):


        self.venues: Dict[int, Venue] = {}



    # =========================================================
    # DATABASE IMPORT
    # =========================================================


    def load_venues(
            self,
            venue_data: List[dict]
    ):


        """
        Convert JSON venue records
        into Venue objects.
        """


        for data in venue_data:


            venue = Venue(

                id=data.get(
                    "id"
                ),

                name=data.get(
                    "name",
                    "Unknown Track"
                ),

                location=data.get(
                    "location",
                    ""
                ),

                track_length=data.get(
                    "track_length",
                    300
                ),

                capacity=data.get(
                    "capacity",
                    0
                ),

                average_crowd=data.get(
                    "average_crowd",
                    0
                ),

                track_type=data.get(
                    "track_type",
                    "Standard"
                ),

                home_advantage=data.get(
                    "home_advantage",
                    1.05
                )

            )


            self.venues[venue.id] = venue



        return len(
            self.venues
        )



    # =========================================================
    # VENUE ACCESS
    # =========================================================


    def get_venue(
            self,
            venue_id: int
    ) -> Optional[Venue]:


        return self.venues.get(
            venue_id
        )



    def search(
            self,
            name: str
    ) -> List[Venue]:


        name = name.lower()


        return [

            venue

            for venue in self.venues.values()

            if name in venue.name.lower()

        ]



    # =========================================================
    # TRACK CHARACTERISTICS
    # =========================================================


    def track_difficulty(
            self,
            venue_id: int
    ):


        venue = self.get_venue(
            venue_id
        )


        if not venue:

            return 1.0



        difficulty = 1.0



        # Longer tracks require stamina

        if venue.track_length >= 400:

            difficulty += 0.10



        # Tight technical tracks

        if venue.track_type == "Technical":

            difficulty += 0.15



        # Large crowds increase pressure

        if venue.capacity >= 15000:

            difficulty += 0.05



        return round(

            difficulty,

            2

        )



    # =========================================================
    # HOME ADVANTAGE
    # =========================================================


    def home_bonus(
            self,
            venue_id: int
    ):


        venue = self.get_venue(
            venue_id
        )


        if not venue:

            return 1.0



        return venue.home_advantage



    # =========================================================
    # WEATHER SYSTEM
    # =========================================================


    def generate_weather(self):


        conditions = [

            "Dry",

            "Cloudy",

            "Light Rain",

            "Heavy Rain",

            "Cold"

        ]


        weather = random.choice(

            conditions

        )


        effects = {


            "Dry":

                1.00,


            "Cloudy":

                0.98,


            "Light Rain":

                0.95,


            "Heavy Rain":

                0.85,


            "Cold":

                0.97

        }



        return {


            "condition":

                weather,


            "performance_modifier":

                effects[weather]

        }



    # =========================================================
    # RIDER TRACK SUITABILITY
    # =========================================================


    def rider_track_bonus(
            self,
            rider,
            venue: Venue
    ):


        """
        Future expansion point.

        Later riders can contain:

        - track_specialist
        - poor_tracks
        - preferred_surface

        """


        bonus = 1.0



        # Experienced riders adapt better

        if rider.age >= 30:

            bonus += 0.02



        # Young riders struggle more on difficult tracks

        if (

            rider.age < 21

            and

            venue.track_type ==
            "Technical"

        ):

            bonus -= 0.05



        return bonus



    # =========================================================
    # ATTENDANCE SYSTEM
    # =========================================================


    def calculate_attendance(
            self,
            venue_id: int,
            importance=1.0
    ):


        venue = self.get_venue(
            venue_id
        )


        if not venue:

            return 0



        crowd = (

            venue.average_crowd

            *

            importance

        )


        variation = random.uniform(

            0.85,

            1.15

        )


        return int(

            crowd * variation

        )



    # =========================================================
    # REPORTING
    # =========================================================


    def venue_report(
            self,
            venue_id
    ):


        venue = self.get_venue(
            venue_id
        )


        if not venue:

            return None



        return {


            "name":

                venue.name,


            "track_length":

                venue.track_length,


            "capacity":

                venue.capacity,


            "average_crowd":

                venue.average_crowd,


            "track_type":

                venue.track_type,


            "home_advantage":

                venue.home_advantage

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    manager = VenueManager()



    test_data = [

        {

            "id":1,

            "name":
                "Belle Vue Hyde Road",

            "location":
                "Manchester",

            "track_length":
                382,

            "capacity":
                30000,

            "average_crowd":
                12000,

            "track_type":
                "Technical",

            "home_advantage":
                1.08

        }

    ]



    manager.load_venues(
        test_data
    )


    print(

        manager.venue_report(1)

    )
