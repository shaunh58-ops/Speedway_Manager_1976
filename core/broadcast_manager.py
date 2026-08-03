"""
Speedway Game Engine

Broadcast Manager Module

Version: 1.0

Controls television, radio and digital broadcasting.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class BroadcastContract:


    broadcaster: str

    start_year: int

    end_year: int

    annual_value: int

    coverage_level: str



@dataclass(slots=True)
class BroadcastEvent:


    season: int

    fixture_id: int

    audience: int

    broadcaster: str

    revenue: int



@dataclass(slots=True)
class BroadcastProfile:


    club_id: int

    exposure: int = 0

    viewers: int = 0

    history: List[BroadcastEvent] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class BroadcastManager:


    def __init__(self):

        self.contracts: List[BroadcastContract] = []

        self.club_profiles: Dict[int, BroadcastProfile] = {}

        self.broadcast_history: List[BroadcastEvent] = []



    # ======================================================
    # PROFILE MANAGEMENT
    # ======================================================


    def get_profile(
            self,
            club_id
    ):


        if club_id not in self.club_profiles:


            self.club_profiles[club_id] = BroadcastProfile(

                club_id=club_id

            )


        return self.club_profiles[club_id]



    # ======================================================
    # BROADCAST EVOLUTION
    # ======================================================


    def media_era(
            self,
            year
    ):


        if year < 1985:

            return "Television Highlights"


        if year < 2000:

            return "Satellite Television"


        if year < 2010:

            return "Professional Broadcast"


        return "Digital Streaming"



    # ======================================================
    # CONTRACT GENERATION
    # ======================================================


    def create_contract(
            self,
            year
    ):


        era = self.media_era(

            year

        )


        values = {


            "Television Highlights":

                50000,


            "Satellite Television":

                250000,


            "Professional Broadcast":

                750000,


            "Digital Streaming":

                1500000

        }



        contract = BroadcastContract(

            broadcaster=era,

            start_year=year,

            end_year=year + 3,

            annual_value=values[era],

            coverage_level=era

        )


        self.contracts.append(

            contract

        )


        return contract



    # ======================================================
    # AUDIENCE CALCULATION
    # ======================================================


    def calculate_audience(
            self,
            club,
            rider_quality,
            importance,
            year
    ):


        base = 10000



        reputation = getattr(

            club,

            "reputation",

            50

        )



        audience = (

            base

            +

            reputation * 200

            +

            rider_quality * 500

            +

            importance * 1000

        )



        multiplier = {


            "Television Highlights":

                1,


            "Satellite Television":

                2,


            "Professional Broadcast":

                4,


            "Digital Streaming":

                8

        }


        audience *= multiplier[

            self.media_era(year)

        ]



        return int(

            audience

        )



    # ======================================================
    # RECORD BROADCAST
    # ======================================================


    def record_broadcast(
            self,
            season,
            fixture_id,
            club_id,
            audience,
            revenue
    ):


        event = BroadcastEvent(

            season=season,

            fixture_id=fixture_id,

            audience=audience,

            broadcaster=self.media_era(

                season

            ),

            revenue=revenue

        )


        self.broadcast_history.append(

            event

        )


        profile = self.get_profile(

            club_id

        )


        profile.exposure += audience // 10000

        profile.viewers += audience


        profile.history.append(

            event

        )


        return event



    # ======================================================
    # REVENUE
    # ======================================================


    def calculate_revenue(
            self,
            audience,
            year
    ):


        rates = {


            "Television Highlights":

                0.05,


            "Satellite Television":

                0.15,


            "Professional Broadcast":

                0.30,


            "Digital Streaming":

                0.50

        }


        return int(

            audience *

            rates[

                self.media_era(year)

            ]

        )



    # ======================================================
    # CHAMPIONSHIP COVERAGE
    # ======================================================


    def championship_exposure(
            self,
            club_id
    ):


        profile = self.get_profile(

            club_id

        )


        profile.exposure += 20


        return profile.exposure



    # ======================================================
    # REPORT
    # ======================================================


    def broadcast_report(
            self,
            club_id
    ):


        profile = self.get_profile(

            club_id

        )


        return {


            "exposure":

                profile.exposure,


            "viewers":

                profile.viewers,


            "events":

                len(profile.history)

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = BroadcastManager()


    contract = manager.create_contract(

        1976

    )


    print(

        contract

    )
