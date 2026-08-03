"""
Speedway Game Engine

Championship Engine Module

Version: 1.0

Controls Speedway championships,
records and historical achievements.

Features:

- League champions
- Rider championships
- Season averages
- Career statistics
- Hall of Fame

"""


from typing import Dict, List


from models import Rider, Club



class ChampionshipEngine:



    def __init__(self):

        self.league_history = {}

        self.rider_history = {}

        self.hall_of_fame = []



    # =========================================================
    # LEAGUE CHAMPIONSHIP
    # =========================================================


    def record_league_champion(
            self,
            season: int,
            club: Club
    ):


        self.league_history[season] = {


            "champion":

                club.name,


            "club_id":

                club.id,


            "points":

                club.points

        }



    def get_league_champion(
            self,
            season: int
    ):


        return self.league_history.get(
            season
        )



    # =========================================================
    # RIDER CHAMPIONSHIP
    # =========================================================


    def calculate_rider_rankings(
            self,
            riders: List[Rider]
    ):


        rankings = sorted(

            riders,

            key=lambda rider:
                rider.current_cma,

            reverse=True

        )


        return rankings



    def award_individual_title(
            self,
            season: int,
            riders: List[Rider]
    ):


        rankings = self.calculate_rider_rankings(

            riders

        )



        if not rankings:

            return None



        champion = rankings[0]



        self.rider_history[season] = {


            "champion":

                champion.name,


            "rider_id":

                champion.id,


            "cma":

                champion.current_cma

        }



        return champion



    # =========================================================
    # RIDER STATISTICS
    # =========================================================


    def calculate_average_cma(
            self,
            rider: Rider,
            meetings: int
    ):


        if meetings == 0:

            return 0



        return round(

            rider.current_cma /
            meetings,

            2

        )



    def rider_profile(
            self,
            rider: Rider
    ):


        return {


            "name":

                rider.name,


            "age":

                rider.age,


            "current_cma":

                rider.current_cma,


            "career_years":

                rider.career_years,


            "retired":

                rider.retired

        }



    # =========================================================
    # HALL OF FAME
    # =========================================================


    def evaluate_legend_status(
            self,
            rider: Rider
    ):


        score = 0



        # Elite CMA

        if rider.current_cma >= 10:

            score += 40



        # Longevity

        if rider.career_years >= 15:

            score += 30



        # Experience

        if rider.age >= 35:

            score += 10



        if score >= 70:


            if rider.name not in self.hall_of_fame:


                self.hall_of_fame.append(

                    rider.name

                )


            return True



        return False



    def get_hall_of_fame(self):

        return self.hall_of_fame



    # =========================================================
    # SEASON REVIEW
    # =========================================================


    def season_review(
            self,
            season: int
    ):


        return {


            "season":

                season,


            "league":

                self.league_history.get(

                    season,

                    None

                ),


            "individual":

                self.rider_history.get(

                    season,

                    None

                )

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    from models import Rider



    riders = [

        Rider(

            1,

            "Legend Rider",

            current_cma=10.5

        ),


        Rider(

            2,

            "Young Star",

            current_cma=8.5

        )

    ]



    engine = ChampionshipEngine()


    champion = engine.award_individual_title(

        1976,

        riders

    )


    print(

        champion.name

    )
