"""
Speedway Game Engine

Transfer Manager Module

Version: 1.0

Controls rider contracts and transfers.

Features:

- Contracts
- Transfers
- Free agents
- Contract renewals
- Transfer history

"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Contract:

    rider_id: int
    club_id: int

    start_year: int
    expiry_year: int

    weekly_wage: int

    loyalty: int = 50


class TransferManager:

    def __init__(self):

        self.contracts: Dict[int, Contract] = {}

        self.transfer_history: List[dict] = []

        self.free_agents = set()

    # =====================================================
    # CONTRACTS
    # =====================================================

    def create_contract(
        self,
        rider,
        club,
        start_year,
        years,
        weekly_wage
    ):

        contract = Contract(

            rider_id=rider.id,

            club_id=club.id,

            start_year=start_year,

            expiry_year=start_year + years,

            weekly_wage=weekly_wage,

            loyalty=50

        )

        self.contracts[rider.id] = contract

        rider.club_id = club.id

        return contract

    def get_contract(
        self,
        rider_id
    ) -> Optional[Contract]:

        return self.contracts.get(rider_id)

    # =====================================================
    # CONTRACT EXPIRY
    # =====================================================

    def contracts_expiring(
        self,
        season
    ):

        return [

            contract

            for contract

            in self.contracts.values()

            if contract.expiry_year <= season

        ]

    # =====================================================
    # FREE AGENTS
    # =====================================================

    def release_rider(
        self,
        rider
    ):

        if rider.id in self.contracts:

            del self.contracts[rider.id]

        rider.club_id = None

        self.free_agents.add(rider.id)

    # =====================================================
    # TRANSFER
    # =====================================================

    def transfer_rider(
        self,
        rider,
        from_club,
        to_club,
        fee,
        season
    ):

        rider.club_id = to_club.id

        self.free_agents.discard(rider.id)

        contract = self.contracts.get(rider.id)

        if contract:

            contract.club_id = to_club.id

            contract.start_year = season

        self.transfer_history.append(

            {

                "season": season,

                "rider": rider.name,

                "from": from_club.name if from_club else None,

                "to": to_club.name,

                "fee": fee

            }

        )

        return True

    # =====================================================
    # CONTRACT RENEWAL
    # =====================================================

    def renew_contract(
        self,
        rider,
        years,
        new_wage
    ):

        contract = self.contracts.get(rider.id)

        if contract is None:

            return False

        contract.expiry_year += years

        contract.weekly_wage = new_wage

        contract.loyalty = min(
            100,
            contract.loyalty + 10
        )

        return True

    # =====================================================
    # AI BID EVALUATION
    # =====================================================

    def evaluate_offer(
        self,
        rider,
        club,
        fee,
        reputation
    ):

        score = 0

        score += fee / 1000

        score += reputation

        contract = self.contracts.get(rider.id)

        if contract:

            score += contract.loyalty * 0.2

        return round(score, 2)

    # =====================================================
    # TRANSFER HISTORY
    # =====================================================

    def history(self):

        return self.transfer_history

    # =====================================================
    # REPORT
    # =====================================================

    def transfer_summary(self):

        return {

            "active_contracts":

                len(self.contracts),

            "free_agents":

                len(self.free_agents),

            "completed_transfers":

                len(self.transfer_history)

        }


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    manager = TransferManager()

    print(

        manager.transfer_summary()

    )
