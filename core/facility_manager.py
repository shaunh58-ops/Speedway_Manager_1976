"""
Speedway Game Engine

Facility Manager Module

Version: 1.0

Controls club infrastructure,
development facilities and investment.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class ClubFacilities:


    club_id: int

    training_level: int = 50

    workshop_level: int = 50

    medical_level: int = 50

    youth_academy_level: int = 50

    track_equipment_level: int = 50

    reputation: int = 50

    investment_history: List[str] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class FacilityManager:


    def __init__(self):

        self.facilities: Dict[int, ClubFacilities] = {}



    # ======================================================
    # PROFILE MANAGEMENT
    # ======================================================


    def get_facilities(
            self,
            club_id
    ):


        if club_id not in self.facilities:


            self.facilities[club_id] = ClubFacilities(

                club_id=club_id

            )


        return self.facilities[club_id]



    # ======================================================
    # INVESTMENT
    # ======================================================


    def upgrade_facility(
            self,
            club_id,
            facility_type
    ):


        facilities = self.get_facilities(

            club_id

        )


        if facility_type == "training":

            facilities.training_level += 10


        elif facility_type == "workshop":

            facilities.workshop_level += 10


        elif facility_type == "medical":

            facilities.medical_level += 10


        elif facility_type == "youth":

            facilities.youth_academy_level += 10


        elif facility_type == "track":

            facilities.track_equipment_level += 10


        else:

            return False



        facilities.investment_history.append(

            facility_type

        )


        self.update_reputation(

            facilities

        )


        self.clamp_values(

            facilities

        )


        return True



    # ======================================================
    # DEVELOPMENT EFFECTS
    # ======================================================


    def rider_training_bonus(
            self,
            club_id
    ):


        facilities = self.get_facilities(

            club_id

        )


        return round(

            facilities.training_level *

            0.05,

            2

        )



    def youth_development_bonus(
            self,
            club_id
    ):


        facilities = self.get_facilities(

            club_id

        )


        return round(

            facilities.youth_academy_level *

            0.08,

            2

        )



    # ======================================================
    # INJURY SUPPORT
    # ======================================================


    def recovery_bonus(
            self,
            club_id
    ):


        facilities = self.get_facilities(

            club_id

        )


        return round(

            facilities.medical_level *

            0.04,

            2

        )



    # ======================================================
    # WORKSHOP EFFECT
    # ======================================================


    def equipment_bonus(
            self,
            club_id
    ):


        facilities = self.get_facilities(

            club_id

        )


        return round(

            facilities.workshop_level *

            0.03,

            2

        )



    # ======================================================
    # REPUTATION
    # ======================================================


    def update_reputation(
            self,
            facilities
    ):


        average = (

            facilities.training_level

            +

            facilities.workshop_level

            +

            facilities.medical_level

            +

            facilities.youth_academy_level

        ) / 4



        facilities.reputation = int(

            average

        )



    # ======================================================
    # MAINTENANCE
    # ======================================================


    def annual_decay(
            self,
            club_id
    ):


        facilities = self.get_facilities(

            club_id

        )


        facilities.training_level -= 2

        facilities.workshop_level -= 2

        facilities.medical_level -= 2

        facilities.track_equipment_level -= 2


        self.clamp_values(

            facilities

        )



    # ======================================================
    # CONTROL
    # ======================================================


    def clamp_values(
            self,
            facilities
    ):


        attributes = [

            "training_level",

            "workshop_level",

            "medical_level",

            "youth_academy_level",

            "track_equipment_level",

            "reputation"

        ]


        for attribute in attributes:


            value = getattr(

                facilities,

                attribute

            )


            setattr(

                facilities,

                attribute,

                max(

                    0,

                    min(

                        100,

                        value

                    )

                )

            )



    # ======================================================
    # REPORT
    # ======================================================


    def facility_report(
            self,
            club_id
    ):


        facilities = self.get_facilities(

            club_id

        )


        return {


            "training":

                facilities.training_level,


            "workshop":

                facilities.workshop_level,


            "medical":

                facilities.medical_level,


            "youth":

                facilities.youth_academy_level,


            "reputation":

                facilities.reputation

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = FacilityManager()


    manager.upgrade_facility(

        1,

        "youth"

    )


    print(

        manager.facility_report(1)

    )
