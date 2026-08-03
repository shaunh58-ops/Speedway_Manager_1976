"""
British League Speedway Manager

World Builder

Version: Alpha 0.1

Creates the complete historical Speedway world.
"""


from __future__ import annotations


from dataclasses import dataclass, field


from typing import Dict



from core.logger import get_logger


from core.databases.rider_database_manager import (
    rider_database_manager,
)


from core.databases.club_database_manager import (
    club_database_manager,
)


from core.databases.fixture_database_manager import (
    fixture_database_manager,
)



log = get_logger(

    "WorldBuilder"

)



# ==========================================================
# GAME WORLD MODEL
# ==========================================================


@dataclass
class SpeedwayWorld:


    riders: Dict = field(

        default_factory=dict

    )


    clubs: Dict = field(

        default_factory=dict

    )


    fixtures: Dict = field(

        default_factory=dict

    )


    season: int = 1976



# ==========================================================
# WORLD BUILDER
# ==========================================================


class WorldBuilder:


    def __init__(self):


        self.world = None



    # ======================================================
    # BUILD WORLD
    ======================================================


    def build(
        self,
        rider_file=None,
        club_file=None,
        fixture_file=None,
    ):


        log.info(

            "Building Speedway World"

        )



        # ---------------------------------
        # Load Historical Databases
        # ---------------------------------


        riders = (

            rider_database_manager.load_database(

                rider_file

            )

        )


        clubs = (

            club_database_manager.load_database(

                club_file

            )

        )


        fixtures = (

            fixture_database_manager.load_database(

                fixture_file

            )

        )



        # ---------------------------------
        # Link Riders To Clubs
        # ---------------------------------


        self.assign_riders_to_clubs(

            clubs,

            riders

        )



        # ---------------------------------
        # Create World
        # ---------------------------------


        self.world = SpeedwayWorld(

            riders=riders,

            clubs=clubs,

            fixtures=fixtures

        )



        log.info(

            "Speedway World Created"

        )



        return self.world



    # ======================================================
    # LINK RIDERS
    ======================================================


    def assign_riders_to_clubs(
        self,
        clubs,
        riders,
    ):


        for club in clubs.values():


            club.riders = [

                rider

                for rider

                in riders.values()

                if rider.club == club.name

            ]



            log.info(

                f"{club.name}: {len(club.riders)} riders"

            )



    # ======================================================
    # WORLD ACCESS
    ======================================================


    def get_world(self):


        return self.world



    # ======================================================
    # VALIDATION
    ======================================================


    def validate_world(self):


        if not self.world:


            return False



        if len(self.world.clubs) == 0:


            return False



        if len(self.world.riders) == 0:


            return False



        if len(self.world.fixtures) == 0:


            return False



        return True



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


world_builder = WorldBuilder()
