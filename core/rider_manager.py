"""
Speedway Game Engine

Rider Manager Module

Version: 1.0

Controls rider careers throughout the simulation.

Features:

- Rider database integration
- Career progression
- CMA management
- Retirement system
- Injuries
- Transfers
- Youth development

"""


import random

from typing import Dict, List, Optional


from models import (
    Rider,
    create_rider_from_json
)



class RiderManager:


    def __init__(self):

        self.riders: Dict[int, Rider] = {}



    # =========================================================
    # DATABASE IMPORT
    # =========================================================


    def load_riders(
            self,
            rider_data: List[Dict]
    ):

        """
        Converts JSON rider records into Rider objects.
        """


        for data in rider_data:


            rider = create_rider_from_json(
                data
            )


            self.riders[rider.id] = rider



        return len(
            self.riders
        )



    # =========================================================
    # SEARCH FUNCTIONS
    # =========================================================


    def get_rider(
            self,
            rider_id: int
    ) -> Optional[Rider]:


        return self.riders.get(
            rider_id
        )



    def search(
            self,
            name: str
    ) -> List[Rider]:


        name = name.lower()


        return [

            rider

            for rider in self.riders.values()

            if name in rider.name.lower()

        ]



    # =========================================================
    # CLUB ASSIGNMENT
    # =========================================================


    def assign_to_club(
            self,
            rider_id: int,
            club_id: int
    ):


        rider = self.get_rider(
            rider_id
        )


        if rider:

            rider.club_id = club_id

            return True


        return False



    # =========================================================
    # CMA DEVELOPMENT SYSTEM
    # =========================================================


    def update_cma(
            self,
            rider_id: int,
            performance_change: float
    ):


        rider = self.get_rider(
            rider_id
        )


        if not rider:

            return False



        rider.current_cma += performance_change



        rider.current_cma = round(

            max(
                rider.current_cma,
                0
            ),

            2

        )


        return True



    def seasonal_development(
            self,
            rider_id: int
    ):


        rider = self.get_rider(
            rider_id
        )


        if not rider:

            return



        # Young riders improve quicker

        if rider.age < 25:


            change = random.uniform(
                0.05,
                0.40
            )


        # Peak years

        elif rider.age < 32:


            change = random.uniform(
                -0.10,
                0.20
            )


        # Veteran decline

        else:


            change = random.uniform(
                -0.50,
                0
            )



        self.update_cma(

            rider_id,

            round(
                change,
                2
            )

        )



    # =========================================================
    # AGE & CAREER MANAGEMENT
    # =========================================================


    def progress_year(
            self
    ):


        for rider in self.riders.values():


            rider.age_one_year()


            self.seasonal_development(
                rider.id
            )



    # =========================================================
    # INJURY SYSTEM
    # =========================================================


    def apply_injury(
            self,
            rider_id: int,
            severity: int
    ):


        rider = self.get_rider(
            rider_id
        )


        if rider:


            rider.injuries += severity


            rider.reduce_form(
                0.15 * severity
            )


            return True


        return False



    def recover_injuries(self):


        for rider in self.riders.values():


            if rider.injuries > 0:


                rider.injuries -= 1



    # =========================================================
    # RETIREMENT MANAGEMENT
    # =========================================================


    def check_retirements(self):


        retired = []


        for rider in self.riders.values():


            chance = (
                rider.retirement_probability()
            )


            roll = random.randint(
                1,
                100
            )


            if roll <= chance:


                rider.retired = True


                retired.append(
                    rider
                )



        return retired



    # =========================================================
    # TRANSFER MARKET
    # =========================================================


    def available_riders(self):


        return [

            rider

            for rider in self.riders.values()

            if rider.club_id is None

            and not rider.retired

        ]



    def release_rider(
            self,
            rider_id: int
    ):


        rider = self.get_rider(
            rider_id
        )


        if rider:


            rider.club_id = None

            return True


        return False



    # =========================================================
    # YOUTH DEVELOPMENT
    # =========================================================


    def create_young_rider(
            self,
            name: str,
            nationality: str
    ):


        new_id = max(
            self.riders.keys(),
            default=0
        ) + 1



        rider = Rider(

            id=new_id,

            name=name,

            nationality=nationality,

            age=random.randint(
                16,
                20
            ),

            historical_cma=3.5,

            current_cma=3.5,

            potential=random.uniform(
                5,
                10
            )

        )


        self.riders[new_id] = rider


        return rider



    # =========================================================
    # STATISTICS
    # =========================================================


    def database_summary(self):


        total = len(
            self.riders
        )


        active = len(

            [
                r

                for r in self.riders.values()

                if not r.retired

            ]

        )


        return {


            "total_riders":
                total,


            "active_riders":
                active,


            "retired_riders":
                total - active

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    manager = RiderManager()


    test_data = [

        {

            "id":1,

            "name":
                "Ivan Mauger",

            "nationality":
                "New Zealand",

            "age":
                36,

            "historical_cma":
                11.45

        }

    ]



    manager.load_riders(
        test_data
    )


    rider = manager.get_rider(
        1
    )


    print(
        rider.name,
        rider.current_cma
    )
