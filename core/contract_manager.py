"""
Speedway Game Engine

Contract Manager Module

Version: 1.0

Controls rider contracts, wages,
renewals and financial commitments.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class RiderContract:


    rider_id: int

    club_id: int

    start_year: int

    end_year: int

    weekly_wage: int

    signing_bonus: int = 0

    loyalty_bonus: int = 0

    performance_bonus: int = 0

    active: bool = True



@dataclass(slots=True)
class ContractNegotiation:


    rider_id: int

    requested_wage: int

    requested_years: int

    happiness: int

    accepted: bool = False



# ==========================================================
# MANAGER
# ==========================================================


class ContractManager:


    def __init__(self):

        self.contracts: List[RiderContract] = []

        self.negotiations: List[ContractNegotiation] = []



    # ======================================================
    # CREATE CONTRACT
    # ======================================================


    def create_contract(
            self,
            rider_id,
            club_id,
            year,
            wage,
            years=2
    ):


        contract = RiderContract(

            rider_id=rider_id,

            club_id=club_id,

            start_year=year,

            end_year=year + years,

            weekly_wage=wage

        )


        self.contracts.append(

            contract

        )


        return contract



    # ======================================================
    # FIND CONTRACT
    # ======================================================


    def get_contract(
            self,
            rider_id
    ):


        for contract in self.contracts:


            if (

                contract.rider_id == rider_id

                and

                contract.active

            ):

                return contract


        return None



    # ======================================================
    # WAGE CALCULATION
    # ======================================================


    def calculate_value(
            self,
            rider
    ):


        value = (

            rider.average *

            2000

        )


        value += (

            rider.reputation *

            100

        )


        value += (

            rider.age_factor *

            500

        )


        return int(

            value

        )



    # ======================================================
    # NEGOTIATION
    # ======================================================


    def negotiate(
            self,
            rider,
            current_contract
    ):


        demand = self.calculate_value(

            rider

        )


        negotiation = ContractNegotiation(

            rider_id=rider.id,

            requested_wage=demand,

            requested_years=2,

            happiness=70

        )


        self.negotiations.append(

            negotiation

        )


        return negotiation



    # ======================================================
    # ACCEPT CONTRACT
    # ======================================================


    def accept_contract(
            self,
            negotiation,
            club_id,
            year
    ):


        contract = self.create_contract(

            negotiation.rider_id,

            club_id,

            year,

            negotiation.requested_wage,

            negotiation.requested_years

        )


        negotiation.accepted = True


        return contract



    # ======================================================
    # CONTRACT EXPIRY
    # ======================================================


    def check_expiring_contracts(
            self,
            year
    ):


        expiring = []


        for contract in self.contracts:


            if contract.end_year <= year:


                expiring.append(

                    contract

                )


        return expiring



    # ======================================================
    # RELEASE RIDER
    # ======================================================


    def terminate_contract(
            self,
            rider_id
    ):


        contract = self.get_contract(

            rider_id

        )


        if contract:


            contract.active = False


            return True



        return False



    # ======================================================
    # WAGE COSTS
    # ======================================================


    def club_wage_bill(
            self,
            club_id
    ):


        total = 0


        for contract in self.contracts:


            if (

                contract.club_id == club_id

                and

                contract.active

            ):


                total += contract.weekly_wage



        return total



    # ======================================================
    # REPORT
    ======================================================


    def contract_report(
            self,
            rider_id
    ):


        contract = self.get_contract(

            rider_id

        )


        if not contract:

            return None



        return {


            "club":

                contract.club_id,


            "expires":

                contract.end_year,


            "weekly_wage":

                contract.weekly_wage

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = ContractManager()


    contract = manager.create_contract(

        1,

        10,

        1976,

        500

    )


    print(

        manager.contract_report(1)

    )
