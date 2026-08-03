"""
Speedway Game Engine

Team Manager Module

Version: 1.0

Controls Speedway clubs and team management.

Features:

- Club creation
- Squad management
- Rider transfers
- Team strength calculation
- Race line-ups
- Club statistics

"""


from typing import Dict, List, Optional


from models import (
    Club,
    Rider,
    create_club_from_json
)



class TeamManager:


    def __init__(self):

        self.clubs: Dict[int, Club] = {}



    # =========================================================
    # CLUB DATABASE IMPORT
    # =========================================================


    def load_clubs(
            self,
            club_data: List[Dict]
    ):


        """
        Convert JSON club data
        into Club objects.
        """


        for data in club_data:


            club = create_club_from_json(
                data
            )


            self.clubs[club.id] = club



        return len(
            self.clubs
        )



    # =========================================================
    # CLUB ACCESS
    # =========================================================


    def get_club(
            self,
            club_id: int
    ) -> Optional[Club]:


        return self.clubs.get(
            club_id
        )



    def search_clubs(
            self,
            name: str
    ) -> List[Club]:


        name = name.lower()


        return [

            club

            for club in self.clubs.values()

            if name in club.name.lower()

        ]



    # =========================================================
    # RIDER SIGNING
    # =========================================================


    def sign_rider(
            self,
            club_id: int,
            rider: Rider
    ):


        club = self.get_club(
            club_id
        )


        if not club:

            return False



        club.add_rider(
            rider
        )


        return True



    def release_rider(
            self,
            club_id: int,
            rider_id: int
    ):


        club = self.get_club(
            club_id
        )


        if not club:

            return False



        club.remove_rider(
            rider_id
        )


        return True



    # =========================================================
    # TEAM STRENGTH
    # =========================================================


    def calculate_team_strength(
            self,
            club_id: int
    ):


        club = self.get_club(
            club_id
        )


        if not club:

            return 0



        riders = [

            rider

            for rider in club.squad

            if not rider.retired

        ]



        if not riders:

            return 0



        strength = sum(

            rider.racing_ability()

            for rider in riders

        )



        return round(
            strength,
            2
        )



    # =========================================================
    # RACE NIGHT LINE-UP
    # =========================================================


    def select_race_team(
            self,
            club_id: int,
            riders_required: int = 7
    ) -> List[Rider]:


        club = self.get_club(
            club_id
        )


        if not club:

            return []



        available = [

            rider

            for rider in club.squad

            if not rider.retired

            and rider.injuries == 0

        ]



        available.sort(

            key=lambda r:
                r.racing_ability(),

            reverse=True

        )



        return available[
            :riders_required
        ]



    # =========================================================
    # TEAM BALANCE
    # =========================================================


    def squad_average_age(
            self,
            club_id: int
    ):


        club = self.get_club(
            club_id
        )


        if not club or not club.squad:

            return 0



        total = sum(

            rider.age

            for rider in club.squad

        )


        return round(

            total /
            len(club.squad),

            1

        )



    def team_report(
            self,
            club_id: int
    ):


        club = self.get_club(
            club_id
        )


        if not club:

            return None



        return {


            "club":

                club.name,


            "riders":

                len(club.squad),


            "average_cma":

                club.team_average_cma(),


            "team_strength":

                self.calculate_team_strength(
                    club_id
                ),


            "average_age":

                self.squad_average_age(
                    club_id
                ),


            "wins":

                club.wins,


            "points":

                club.points

        }



    # =========================================================
    # TRANSFER MARKET
    # =========================================================


    def transfer_rider(
            self,
            rider: Rider,
            from_club: int,
            to_club: int
    ):


        old_team = self.get_club(
            from_club
        )


        new_team = self.get_club(
            to_club
        )


        if not old_team or not new_team:

            return False



        old_team.remove_rider(
            rider.id
        )


        new_team.add_rider(
            rider
        )


        return True



    # =========================================================
    # SEASON MANAGEMENT
    # =========================================================


    def reset_season_statistics(self):


        for club in self.clubs.values():


            club.wins = 0

            club.defeats = 0

            club.points = 0



    # =========================================================
    # LEAGUE SUMMARY
    # =========================================================


    def league_table(self):


        return sorted(

            self.clubs.values(),

            key=lambda club:
                club.points,

            reverse=True

        )



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    manager = TeamManager()



    clubs = [

        {

            "id":1,

            "name":
                "Wolverhampton Wolves",

            "location":
                "Wolverhampton",

            "founded":
                1928

        }

    ]



    manager.load_clubs(
        clubs
    )



    print(

        manager.get_club(1).name

    )
