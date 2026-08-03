"""
Speedway Game Engine

Coach Manager Module

Version: 1.0

Controls team managers, coaches,
mechanics and staff influence.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class Coach:


    id: int

    name: str

    role: str

    tactical_skill: int

    development_skill: int

    motivation_skill: int

    reputation: int = 50

    experience: int = 1



@dataclass(slots=True)
class StaffContract:


    coach_id: int

    club_id: int

    start_year: int

    end_year: int

    salary: int



@dataclass(slots=True)
class ClubStaff:


    club_id: int

    coaches: List[int] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class CoachManager:


    def __init__(self):

        self.coaches: Dict[int, Coach] = {}

        self.contracts: List[StaffContract] = []

        self.club_staff: Dict[int, ClubStaff] = {}

        self.next_id = 1



    # ======================================================
    # CREATE COACH
    # ======================================================


    def create_coach(
            self,
            name,
            role
    ):


        coach = Coach(

            id=self.next_id,

            name=name,

            role=role,

            tactical_skill=random.randint(

                40,

                90

            ),

            development_skill=random.randint(

                40,

                90

            ),

            motivation_skill=random.randint(

                40,

                90

            ),

            reputation=random.randint(

                30,

                80

            )

        )


        self.coaches[coach.id] = coach


        self.next_id += 1


        return coach



    # ======================================================
    # STAFF ASSIGNMENT
    # ======================================================


    def assign_coach(
            self,
            club_id,
            coach_id,
            season,
            years=3
    ):


        if club_id not in self.club_staff:


            self.club_staff[club_id] = ClubStaff(

                club_id=club_id

            )



        self.club_staff[club_id].coaches.append(

            coach_id

        )


        contract = StaffContract(

            coach_id=coach_id,

            club_id=club_id,

            start_year=season,

            end_year=season + years,

            salary=5000

        )


        self.contracts.append(

            contract

        )


        return contract



    # ======================================================
    # CLUB BONUS CALCULATIONS
    # ======================================================


    def coaching_bonus(
            self,
            club_id
    ):


        staff = self.club_staff.get(

            club_id

        )


        if not staff:

            return 0



        total = 0


        for coach_id in staff.coaches:


            coach = self.coaches[coach_id]


            total += (

                coach.development_skill

                +

                coach.motivation_skill

            )



        return round(

            total /

            len(staff.coaches)

            /

            20,

            2

        )



    # ======================================================
    # TACTICAL SUPPORT
    # ======================================================


    def race_strategy_bonus(
            self,
            club_id
    ):


        staff = self.club_staff.get(

            club_id

        )


        if not staff:

            return 0



        tactical = []


        for coach_id in staff.coaches:


            tactical.append(

                self.coaches[coach_id].tactical_skill

            )



        return round(

            sum(tactical)

            /

            len(tactical)

            /

            10,

            2

        )



    # ======================================================
    # EXPERIENCE DEVELOPMENT
    # ======================================================


    def improve_staff(
            self,
            coach_id
    ):


        coach = self.coaches.get(

            coach_id

        )


        if not coach:

            return



        coach.experience += 1


        coach.reputation += 1


        coach.reputation = min(

            100,

            coach.reputation

        )



    # ======================================================
    # REPORT
    # ======================================================


    def coach_report(
            self,
            coach_id
    ):


        coach = self.coaches.get(

            coach_id

        )


        if not coach:

            return None



        return {


            "name":

                coach.name,


            "role":

                coach.role,


            "tactical":

                coach.tactical_skill,


            "development":

                coach.development_skill,


            "reputation":

                coach.reputation

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = CoachManager()


    coach = manager.create_coach(

        "John Anderson",

        "Team Manager"

    )


    manager.assign_coach(

        1,

        coach.id,

        1976

    )


    print(

        manager.coach_report(

            coach.id

        )

    )
