"""
Speedway Game Engine

Ranking Manager Module

Version: 1.0

Controls dynamic rider and club rankings.

Features:

- Rider rankings
- Club rankings
- Reputation
- Form tracking
- AI evaluation

"""


from __future__ import annotations

from typing import Dict, List


class RankingManager:


    def __init__(self):


        self.rider_rankings: Dict[int, float] = {}

        self.club_rankings: Dict[int, float] = {}

        self.rider_form: Dict[int, List[int]] = {}



    # ======================================================
    # RIDER RATING
    # ======================================================


    def calculate_rider_rating(
            self,
            rider
    ):


        rating = 0



        # Current ability

        rating += (

            rider.current_cma *

            10

        )



        # Experience bonus

        rating += (

            min(

                rider.experience,

                100

            )

            *

            0.05

        )



        # Achievement bonus

        rating += (

            getattr(

                rider,

                "championships",

                0

            )

            *

            5

        )



        # World titles

        rating += (

            getattr(

                rider,

                "world_titles",

                0

            )

            *

            10

        )



        # Recent form

        rating += self.form_bonus(

            rider.id

        )



        # Age effect

        if rider.age > 38:

            rating -= 5



        return round(

            rating,

            2

        )



    # ======================================================
    # UPDATE RIDER RANKINGS
    # ======================================================


    def update_rider_rankings(
            self,
            riders
    ):


        rankings = {}



        for rider in riders:


            if rider.retired:

                continue



            rankings[rider.id] = self.calculate_rider_rating(

                rider

            )



        self.rider_rankings = rankings



        return self.top_riders()



    # ======================================================
    # TOP RIDERS
    # ======================================================


    def top_riders(
            self,
            limit=20
    ):


        return sorted(

            self.rider_rankings.items(),

            key=lambda x: x[1],

            reverse=True

        )[:limit]



    # ======================================================
    # FORM SYSTEM
    # ======================================================


    def record_result(
            self,
            rider_id,
            points
    ):


        if rider_id not in self.rider_form:


            self.rider_form[rider_id] = []



        self.rider_form[rider_id].append(

            points

        )



        # Keep last 10 rides


        self.rider_form[rider_id] = (

            self.rider_form[rider_id][-10:]

        )



    def form_bonus(
            self,
            rider_id
    ):


        results = self.rider_form.get(

            rider_id,

            []

        )


        if not results:

            return 0



        average = sum(results) / len(results)



        return round(

            average *

            0.25,

            2

        )



    # ======================================================
    # CLUB RANKINGS
    # ======================================================


    def calculate_club_rating(
            self,
            club
    ):


        rating = 0



        rating += (

            getattr(

                club,

                "league_titles",

                0

            )

            *

            10

        )



        rating += (

            getattr(

                club,

                "reputation",

                50

            )

        )



        rating += (

            getattr(

                club,

                "financial_balance",

                0

            )

            /

            100000

        )



        return round(

            rating,

            2

        )



    def update_club_rankings(
            self,
            clubs
    ):


        rankings = {}



        for club in clubs:


            rankings[club.id] = self.calculate_club_rating(

                club

            )



        self.club_rankings = rankings



        return self.top_clubs()



    def top_clubs(
            self,
            limit=10
    ):


        return sorted(

            self.club_rankings.items(),

            key=lambda x: x[1],

            reverse=True

        )[:limit]



    # ======================================================
    # REPUTATION
    # ======================================================


    def reputation_level(
            self,
            rating
    ):


        if rating >= 90:

            return "Elite"



        if rating >= 75:

            return "Strong"



        if rating >= 60:

            return "Established"



        if rating >= 40:

            return "Developing"



        return "Unknown"



    # ======================================================
    # REPORT
    # ======================================================


    def ranking_report(self):


        return {


            "top_riders":

                self.top_riders(),


            "top_clubs":

                self.top_clubs()

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = RankingManager()


    print(

        "Ranking Manager Loaded"

    )
