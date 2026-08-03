"""
Speedway Game Engine

Transfer Window Manager Module

Version: 1.0

Controls rider transfers, recruitment,
fees and movement history.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class TransferListing:


    rider_id: int

    current_club: int | None

    asking_price: int

    available: bool = True

    reason: str = ""



@dataclass(slots=True)
class TransferRecord:


    rider_id: int

    old_club: int | None

    new_club: int

    fee: int

    season: int

    transfer_type: str



@dataclass(slots=True)
class LoanAgreement:


    rider_id: int

    parent_club: int

    loan_club: int

    start_year: int

    end_year: int



# ==========================================================
# MANAGER
# ==========================================================


class TransferWindowManager:


    def __init__(self):

        self.market: Dict[int, TransferListing] = {}

        self.history: List[TransferRecord] = []

        self.loans: List[LoanAgreement] = []



    # ======================================================
    # LIST RIDER
    # ======================================================


    def list_rider(
            self,
            rider_id,
            club_id,
            value,
            reason=""
    ):


        listing = TransferListing(

            rider_id=rider_id,

            current_club=club_id,

            asking_price=value,

            reason=reason

        )


        self.market[rider_id] = listing


        return listing



    # ======================================================
    # MARKET VALUE
    # ======================================================


    def calculate_market_value(
            self,
            rider
    ):


        value = 0


        value += getattr(

            rider,

            "average",

            5

        ) * 15000



        value += getattr(

            rider,

            "reputation",

            50

        ) * 2000



        age = getattr(

            rider,

            "age",

            25

        )


        if age < 23:


            value *= 1.25



        elif age > 35:


            value *= 0.7



        return int(

            value

        )



    # ======================================================
    # TRANSFER COMPLETION
    # ======================================================


    def complete_transfer(
            self,
            rider_id,
            new_club,
            season
    ):


        listing = self.market.get(

            rider_id

        )


        if not listing:

            return None



        record = TransferRecord(

            rider_id=rider_id,

            old_club=listing.current_club,

            new_club=new_club,

            fee=listing.asking_price,

            season=season,

            transfer_type="Permanent"

        )


        self.history.append(

            record

        )


        listing.available = False


        return record



    # ======================================================
    # FREE AGENTS
    # ======================================================


    def create_free_agent(
            self,
            rider_id,
            value
    ):


        return self.list_rider(

            rider_id,

            None,

            value,

            "Free Agent"

        )



    # ======================================================
    # LOANS
    # ======================================================


    def create_loan(
            self,
            rider_id,
            parent_club,
            loan_club,
            year,
            duration=1
    ):


        loan = LoanAgreement(

            rider_id=rider_id,

            parent_club=parent_club,

            loan_club=loan_club,

            start_year=year,

            end_year=year + duration

        )


        self.loans.append(

            loan

        )


        return loan



    # ======================================================
    # SEARCH MARKET
    # ======================================================


    def available_riders(
            self
    ):


        return [

            listing

            for listing

            in self.market.values()

            if listing.available

        ]



    # ======================================================
    # REMOVE LISTING
    # ======================================================


    def remove_listing(
            self,
            rider_id
    ):


        if rider_id in self.market:


            del self.market[rider_id]


            return True


        return False



    # ======================================================
    # CLUB TRANSFER REPORT
    # ======================================================


    def club_transfers(
            self,
            club_id
    ):


        return [

            transfer

            for transfer

            in self.history

            if (

                transfer.old_club == club_id

                or

                transfer.new_club == club_id

            )

        ]



    # ======================================================
    # REPORT
    # ======================================================


    def market_report(
            self
    ):


        return [

            {

                "rider":

                    listing.rider_id,


                "value":

                    listing.asking_price,


                "reason":

                    listing.reason

            }

            for listing

            in self.available_riders()

        ]



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = TransferWindowManager()


    manager.list_rider(

        1,

        10,

        50000,

        "Wants new challenge"

    )


    print(

        manager.market_report()

    )
