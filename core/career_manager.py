"""
Speedway Game Engine

Career Manager Module

Version: 1.0

Controls player management careers.

Features:

- Manager profile
- Club employment
- Reputation
- Objectives
- Job offers
- Career history

"""


from typing import List, Dict



class CareerManager:



    def __init__(
            self,
            manager_name
    ):


        self.manager_name = manager_name


        self.current_club = None


        self.start_year = None


        self.current_year = None


        self.experience = 0


        self.reputation = 20


        self.trophies = []


        self.history = []


        self.job_offers = []



    # =========================================================
    # START CAREER
    # =========================================================


    def start_career(
            self,
            club,
            year
    ):


        self.current_club = club


        self.start_year = year


        self.current_year = year



        self.history.append(

            {

                "year":

                    year,


                "event":

                    f"Started career at {club.name}"

            }

        )



        return True



    # =========================================================
    # PROFILE
    # =========================================================


    def profile(self):


        return {


            "manager":

                self.manager_name,


            "club":

                self.current_club.name

                if self.current_club

                else None,


            "experience":

                self.experience,


            "reputation":

                self.reputation,


            "trophies":

                len(self.trophies)

        }



    # =========================================================
    # SEASON PROCESSING
    # =========================================================


    def complete_season(
            self,
            position,
            trophies_won=None
    ):


        self.current_year += 1


        self.experience += 1



        reputation_gain = 0



        if position == 1:

            reputation_gain += 20



        elif position <= 3:

            reputation_gain += 10



        else:

            reputation_gain += 2



        self.reputation += reputation_gain



        if trophies_won:


            for trophy in trophies_won:


                self.trophies.append(

                    {

                    "year":

                        self.current_year,


                    "trophy":

                        trophy

                    }

                )



                self.reputation += 5



        self.history.append(

            {

            "year":

                self.current_year,


            "position":

                position

            }

        )



    # =========================================================
    # CLUB OBJECTIVES
    # =========================================================


    def generate_objective(
            self,
            club
    ):


        objectives = {


            "top_team":

                "Win the league",


            "mid_team":

                "Finish top half",


            "small_team":

                "Avoid bottom position"

        }



        strength = club.team_average_cma()



        if strength >= 55:


            return objectives["top_team"]



        elif strength >= 40:


            return objectives["mid_team"]



        else:


            return objectives["small_team"]



    # =========================================================
    # JOB OFFERS
    # =========================================================


    def evaluate_job_offers(
            self,
            clubs: List
    ):


        offers = []



        for club in clubs:


            strength = club.team_average_cma()



            required = strength / 2



            if self.reputation >= required:


                offers.append(

                    club

                )



        self.job_offers = offers



        return offers



    # =========================================================
    # CHANGE CLUB
    # =========================================================


    def accept_job(
            self,
            club
    ):


        previous = self.current_club



        self.current_club = club



        self.history.append(

            {

            "year":

                self.current_year,


            "event":

                f"Moved from {previous.name if previous else 'none'} to {club.name}"

            }

        )



        return True



    # =========================================================
    # CAREER SUMMARY
    # =========================================================


    def career_summary(self):


        return {


            "manager":

                self.manager_name,


            "years":

                self.current_year -
                self.start_year
                if self.start_year
                else 0,


            "experience":

                self.experience,


            "reputation":

                self.reputation,


            "trophies":

                self.trophies,


            "history":

                self.history

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    manager = CareerManager(

        "Speedway Manager"

    )


    print(

        manager.profile()

    )
