"""
Speedway Game Engine

Scouting Manager Module

Version: 1.0

Manages rider scouting and youth development.

Features:

- Youth generation
- Scout reports
- Regional scouting
- Overseas scouting
- Prospect rankings

"""

import random
from typing import Dict, List


class ScoutingManager:

    REGIONS = [
        "England",
        "Scotland",
        "Wales",
        "Australia",
        "New Zealand",
        "Sweden",
        "Denmark",
        "Poland",
        "USA"
    ]

    FIRST_NAMES = [
        "Chris", "Mark", "David", "Alan",
        "Jason", "Paul", "Steve", "Kevin",
        "Michael", "Scott", "Gary", "Neil"
    ]

    LAST_NAMES = [
        "Anderson", "Smith", "Johnson",
        "Wilson", "Taylor", "Collins",
        "Nicholls", "Carter", "Richardson",
        "Jenkins", "Brown", "Cook"
    ]

    TRACK_TYPES = [
        "Technical",
        "Fast",
        "Long",
        "Short",
        "Balanced"
    ]

    def __init__(self):

        self.prospects: Dict[int, dict] = {}

        self.next_id = 100000

    # =====================================================
    # PROSPECT CREATION
    # =====================================================

    def generate_prospect(self):

        rider = {

            "id": self.next_id,

            "name":
                f"{random.choice(self.FIRST_NAMES)} "
                f"{random.choice(self.LAST_NAMES)}",

            "age":
                random.randint(16, 20),

            "nationality":
                random.choice(self.REGIONS),

            "current_cma":
                round(
                    random.uniform(2.5, 5.5),
                    2
                ),

            "potential":
                round(
                    random.uniform(6.0, 10.5),
                    2
                ),

            "development_rate":
                random.choice(
                    [
                        "Slow",
                        "Normal",
                        "Fast"
                    ]
                ),

            "preferred_track":
                random.choice(
                    self.TRACK_TYPES
                ),

            "scouted":
                False

        }

        self.prospects[self.next_id] = rider

        self.next_id += 1

        return rider

    # =====================================================
    # YEARLY INTAKE
    # =====================================================

    def annual_youth_intake(
            self,
            number=25
    ):

        intake = []

        for _ in range(number):

            intake.append(

                self.generate_prospect()

            )

        return intake

    # =====================================================
    # SCOUT REPORT
    # =====================================================

    def scout_rider(
            self,
            rider
    ):

        rider["scouted"] = True

        rating = self.grade_potential(

            rider["potential"]

        )

        return {

            "name":
                rider["name"],

            "age":
                rider["age"],

            "current_cma":
                rider["current_cma"],

            "potential":
                rider["potential"],

            "development":
                rider["development_rate"],

            "track":
                rider["preferred_track"],

            "recommendation":
                rating

        }

    # =====================================================
    # POTENTIAL GRADE
    # =====================================================

    def grade_potential(
            self,
            potential
    ):

        if potential >= 10:

            return "Generational Talent"

        if potential >= 9:

            return "Outstanding"

        if potential >= 8:

            return "Excellent"

        if potential >= 7:

            return "Good Prospect"

        return "Development Rider"

    # =====================================================
    # SEARCH
    # =====================================================

    def search_region(
            self,
            region
    ):

        return [

            rider

            for rider

            in self.prospects.values()

            if rider["nationality"] == region

        ]

    # =====================================================
    # TOP PROSPECTS
    # =====================================================

    def top_prospects(
            self,
            limit=10
    ):

        prospects = sorted(

            self.prospects.values(),

            key=lambda r: r["potential"],

            reverse=True

        )

        return prospects[:limit]

    # =====================================================
    # SIGN PROSPECT
    # =====================================================

    def sign_prospect(
            self,
            rider_id
    ):

        return self.prospects.pop(

            rider_id,

            None

        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def scouting_summary(self):

        return {

            "prospects":

                len(self.prospects),

            "elite":

                len(

                    [

                        r

                        for r

                        in self.prospects.values()

                        if r["potential"] >= 9

                    ]

                )

        }


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    manager = ScoutingManager()

    manager.annual_youth_intake()

    print(

        manager.scouting_summary()

    )

    print(

        manager.top_prospects(5)

    )
