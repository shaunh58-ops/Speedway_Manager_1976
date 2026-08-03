"""
Speedway Game Engine

Sponsorship Manager Module

Version: 1.0

Controls sponsorship contracts and commercial income.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class SponsorContract:


    sponsor_name: str

    club_id: int

    start_year: int

    expiry_year: int

    annual_value: int

    satisfaction: int = 70

    performance_bonus: int = 0



@dataclass(slots=True)
class RiderSponsor:


    sponsor_name: str

    rider_id: int

    annual_value: int

    popularity_requirement: int



# ==========================================================
# MANAGER
# ==========================================================


class SponsorshipManager:


    def __init__(self):


        self.club_sponsors: Dict[int, SponsorContract] = {}

        self.rider_sponsors: Dict[int, List[RiderSponsor]] = {}

        self.sponsor_history = []



    # ======================================================
    # GENERATE SPONSOR
    # ======================================================


    def generate_sponsor_name(self):


        companies = [

            "SpeedTech",

            "Racing Oils",

            "Northern Engineering",

            "Victory Motors",

            "TrackMaster",

            "Elite Sportswear",

            "PowerFuel"

        ]


        return random.choice(companies)



    # ======================================================
    # OFFER CALCULATION
    # ======================================================


    def calculate_offer(
            self,
            club
    ):


        reputation = getattr(

            club,

            "reputation",

            50

        )


        titles = getattr(

            club,

            "league_titles",

            0

        )


        attendance = getattr(

            club,

            "average_attendance",

            3000

        )


        value = (

            reputation * 1000

            +

            titles * 25000

            +

            attendance * 5

        )


        return int(value)



    # ======================================================
    # CREATE CONTRACT
    # ======================================================


    def sign_club_sponsor(
            self,
            club,
            season,
            years=3
    ):


        contract = SponsorContract(

            sponsor_name=self.generate_sponsor_name(),

            club_id=club.id,

            start_year=season,

            expiry_year=season + years,

            annual_value=self.calculate_offer(club)

        )


        self.club_sponsors[club.id] = contract


        self.sponsor_history.append(contract)


        return contract



    # ======================================================
    # RENEWAL
    # ======================================================


    def renew_contract(
            self,
            club_id,
            season
    ):


        contract = self.club_sponsors.get(

            club_id

        )


        if not contract:

            return False



        contract.expiry_year = season + 3


        contract.satisfaction = min(

            100,

            contract.satisfaction + 10

        )


        return True



    # ======================================================
    # PERFORMANCE REVIEW
    # ======================================================


    def update_satisfaction(
            self,
            club,
            league_position
    ):


        contract = self.club_sponsors.get(

            club.id

        )


        if not contract:

            return



        if league_position <= 3:

            contract.satisfaction += 10


        elif league_position >= 10:

            contract.satisfaction -= 15



        contract.satisfaction = max(

            0,

            min(

                contract.satisfaction,

                100

            )

        )



    # ======================================================
    # RIDER SPONSORS
    # ======================================================


    def sign_rider_sponsor(
            self,
            rider
    ):


        popularity = getattr(

            rider,

            "popularity",

            50

        )


        sponsor = RiderSponsor(

            sponsor_name=self.generate_sponsor_name(),

            rider_id=rider.id,

            annual_value=int(

                popularity * 500

            ),

            popularity_requirement=50

        )


        if rider.id not in self.rider_sponsors:


            self.rider_sponsors[rider.id] = []



        self.rider_sponsors[rider.id].append(

            sponsor

        )


        return sponsor



    # ======================================================
    # INCOME
    # ======================================================


    def annual_income(
            self,
            club_id
    ):


        contract = self.club_sponsors.get(

            club_id

        )


        if not contract:

            return 0



        return contract.annual_value



    # ======================================================
    # REPORTS
    # ======================================================


    def sponsor_report(
            self,
            club_id
    ):


        contract = self.club_sponsors.get(

            club_id

        )


        if not contract:

            return None



        return {


            "sponsor":

                contract.sponsor_name,


            "annual_value":

                contract.annual_value,


            "satisfaction":

                contract.satisfaction,


            "expires":

                contract.expiry_year

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = SponsorshipManager()


    print(

        "Sponsorship Manager Loaded"

    )
