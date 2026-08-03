"""
Speedway Game Engine

Financial Manager Module

Version: 1.0

Controls Speedway club finances.

Features:

- Budgets
- Wages
- Income
- Expenses
- Sponsorship
- Financial reports

"""


from typing import Dict

import random



class FinancialManager:



    def __init__(self):


        self.club_accounts: Dict[int, dict] = {}



    # =========================================================
    # CREATE ACCOUNT
    # =========================================================


    def create_account(
            self,
            club
    ):


        self.club_accounts[club.id] = {


            "club":

                club.name,


            "balance":

                100000,


            "income":

                0,


            "expenses":

                0,


            "sponsorship":

                25000

        }



        return True



    # =========================================================
    # ACCOUNT ACCESS
    # =========================================================


    def get_account(
            self,
            club_id
    ):


        return self.club_accounts.get(

            club_id

        )



    # =========================================================
    # RIDER WAGES
    # =========================================================


    def calculate_wage(
            self,
            rider
    ):


        base = 5000



        cma_bonus = (

            rider.current_cma *

            750

        )



        experience_bonus = (

            rider.age *

            50

        )



        return int(

            base +

            cma_bonus +

            experience_bonus

        )



    def pay_rider_wages(
            self,
            club
    ):


        account = self.get_account(

            club.id

        )



        if not account:

            return 0



        wages = sum(

            self.calculate_wage(

                rider

            )

            for rider

            in club.squad

        )



        account["expenses"] += wages


        account["balance"] -= wages



        return wages



    # =========================================================
    # MATCHDAY INCOME
    # =========================================================


    def calculate_gate_income(
            self,
            venue,
            result=None
    ):


        attendance = venue.average_crowd



        ticket_price = 8



        income = (

            attendance *

            ticket_price

        )



        # Successful teams attract more fans

        if result == "win":


            income *= 1.10



        return int(

            income

        )



    def add_match_income(
            self,
            club,
            amount
    ):


        account = self.get_account(

            club.id

        )


        if account:


            account["income"] += amount


            account["balance"] += amount



    # =========================================================
    # SPONSORSHIP
    # =========================================================


    def update_sponsorship(
            self,
            club,
            reputation
    ):


        account = self.get_account(

            club.id

        )


        if not account:

            return 0



        sponsorship = (

            20000 +

            reputation *

            1000

        )



        variation = random.uniform(

            0.9,

            1.1

        )


        sponsorship *= variation



        account["sponsorship"] = int(

            sponsorship

        )


        account["income"] += int(

            sponsorship

        )


        account["balance"] += int(

            sponsorship

        )



        return int(

            sponsorship

        )



    # =========================================================
    # STADIUM COSTS
    # =========================================================


    def stadium_costs(
            self,
            venue
    ):


        return int(

            venue.capacity *

            0.5

        )



    def pay_stadium_costs(
            self,
            club,
            venue
    ):


        account = self.get_account(

            club.id

        )


        if account:


            cost = self.stadium_costs(

                venue

            )


            account["expenses"] += cost


            account["balance"] -= cost



            return cost



        return 0



    # =========================================================
    # TRANSFER FEES
    # =========================================================


    def transfer_value(
            self,
            rider
    ):


        return int(

            rider.current_cma *

            rider.potential *

            1000

        )



    def pay_transfer_fee(
            self,
            club,
            rider
    ):


        account = self.get_account(

            club.id

        )


        fee = self.transfer_value(

            rider

        )


        if account:


            account["expenses"] += fee


            account["balance"] -= fee



        return fee



    # =========================================================
    # FINANCIAL REPORT
    # =========================================================


    def financial_report(
            self,
            club_id
    ):


        account = self.get_account(

            club_id

        )


        if not account:

            return None



        return {


            "club":

                account["club"],


            "balance":

                account["balance"],


            "income":

                account["income"],


            "expenses":

                account["expenses"],


            "financial_status":

                self.status(

                    account["balance"]

                )

        }



    def status(
            self,
            balance
    ):


        if balance < 0:

            return "Critical"



        elif balance < 25000:

            return "Warning"



        elif balance > 250000:

            return "Healthy"



        return "Stable"



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    finance = FinancialManager()


    print(

        "Financial Manager Loaded"

    )
