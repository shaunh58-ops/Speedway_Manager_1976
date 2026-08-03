"""
Speedway Game Engine

Equipment Manager Module

Version: 1.0

Controls rider machinery,
bike development and reliability.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class RiderEquipment:


    rider_id: int

    engine_power: int

    reliability: int

    setup_quality: int

    maintenance: int

    development_level: int

    factory_support: int

    failures: int = 0

    upgrades: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class EquipmentManager:


    def __init__(self):

        self.equipment: Dict[int, RiderEquipment] = {}



    # ======================================================
    # CREATE EQUIPMENT PROFILE
    # ======================================================


    def create_equipment(
            self,
            rider_id,
            quality=70
    ):


        profile = RiderEquipment(

            rider_id=rider_id,

            engine_power=quality,

            reliability=quality,

            setup_quality=quality,

            maintenance=quality,

            development_level=1,

            factory_support=0

        )


        self.equipment[rider_id] = profile


        return profile



    # ======================================================
    # PERFORMANCE CALCULATION
    # ======================================================


    def performance_bonus(
            self,
            rider_id
    ):


        bike = self.equipment[rider_id]


        score = (

            bike.engine_power * 0.35

            +

            bike.setup_quality * 0.25

            +

            bike.development_level * 5

            +

            bike.factory_support * 0.15

        )


        return round(

            score / 10,

            2

        )



    # ======================================================
    # FAILURE CHECK
    # ======================================================


    def mechanical_failure(
            self,
            rider_id
    ):


        bike = self.equipment[rider_id]


        failure_chance = 100 - bike.reliability


        roll = random.randint(

            1,

            100

        )


        if roll <= failure_chance:


            bike.failures += 1


            return True



        return False



    # ======================================================
    # UPGRADE EQUIPMENT
    # ======================================================


    def upgrade(
            self,
            rider_id,
            upgrade_type
    ):


        bike = self.equipment[rider_id]


        if upgrade_type == "engine":


            bike.engine_power = min(

                100,

                bike.engine_power + 5

            )


        elif upgrade_type == "reliability":


            bike.reliability = min(

                100,

                bike.reliability + 5

            )


        elif upgrade_type == "setup":


            bike.setup_quality = min(

                100,

                bike.setup_quality + 5

            )


        else:

            return False



        bike.upgrades.append(

            upgrade_type

        )


        return True



    # ======================================================
    # FACTORY SUPPORT
    # ======================================================


    def add_factory_support(
            self,
            rider_id,
            level
    ):


        bike = self.equipment[rider_id]


        bike.factory_support = min(

            100,

            bike.factory_support + level

        )



    # ======================================================
    # SEASON DEVELOPMENT
    # ======================================================


    def develop_equipment(
            self,
            rider_id
    ):


        bike = self.equipment[rider_id]


        bike.development_level += 1


        bike.engine_power = min(

            100,

            bike.engine_power + 1

        )


        bike.reliability = min(

            100,

            bike.reliability + 1

        )



    # ======================================================
    # RESET
    # ======================================================


    def repair_season_end(
            self,
            rider_id
    ):


        bike = self.equipment[rider_id]


        bike.failures = 0



    # ======================================================
    # REPORT
    # ======================================================


    def equipment_report(
            self,
            rider_id
    ):


        bike = self.equipment.get(

            rider_id

        )


        if not bike:

            return None



        return {


            "engine":

                bike.engine_power,


            "reliability":

                bike.reliability,


            "setup":

                bike.setup_quality,


            "factory_support":

                bike.factory_support,


            "failures":

                bike.failures,


            "upgrades":

                bike.upgrades

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = EquipmentManager()


    manager.create_equipment(

        1,

        75

    )


    manager.upgrade(

        1,

        "engine"

    )


    print(

        manager.equipment_report(

            1

        )

    )
