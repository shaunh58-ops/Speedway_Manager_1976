"""
Speedway Game Engine
Models Module

Version: 1.0

Contains the core game objects:

    Rider
    Club
    Fixture
    Venue

Designed for historical Speedway simulation.

"""


from dataclasses import dataclass, field
from typing import List, Dict, Optional


# =============================================================
# RIDER MODEL
# =============================================================


@dataclass
class Rider:


    id: int

    name: str

    nationality: str = "Unknown"

    age: int = 18

    historical_cma: float = 0.0

    current_cma: float = 0.0

    potential: float = 0.0

    experience: int = 0

    injuries: int = 0

    retired: bool = False

    club_id: Optional[int] = None

    career_years: int = 0

    form: float = 1.0



    # ---------------------------------------------------------
    # Career Development
    # ---------------------------------------------------------

    def age_one_year(self):

        self.age += 1

        self.career_years += 1

        self.update_retirement_status()



    def improve_form(
            self,
            amount: float
    ):

        self.form += amount

        self.form = min(
            self.form,
            1.5
        )



    def reduce_form(
            self,
            amount: float
    ):

        self.form -= amount

        self.form = max(
            self.form,
            0.5
        )



    # ---------------------------------------------------------
    # Retirement Logic
    # ---------------------------------------------------------

    def retirement_probability(self):

        probability = 0


        if self.age >= 35:

            probability += (
                self.age - 34
            ) * 5


        if self.injuries > 3:

            probability += 15


        return min(
            probability,
            90
        )



    def update_retirement_status(self):

        if self.age >= 45:

            self.retired = True



    # ---------------------------------------------------------
    # Racing Ability
    # ---------------------------------------------------------

    def racing_ability(self):

        ability = (

            self.current_cma *

            self.form

        )


        if self.retired:

            return 0


        return round(
            ability,
            2
        )



# =============================================================
# CLUB MODEL
# =============================================================


@dataclass
class Club:


    id: int

    name: str

    location: str

    founded: int

    stadium: str = ""

    league: str = ""

    capacity: int = 0

    squad: List[Rider] = field(
        default_factory=list
    )

    wins: int = 0

    defeats: int = 0

    points: int = 0



    # ---------------------------------------------------------
    # Squad Management
    # ---------------------------------------------------------


    def add_rider(
            self,
            rider: Rider
    ):

        self.squad.append(
            rider
        )

        rider.club_id = self.id



    def remove_rider(
            self,
            rider_id: int
    ):


        self.squad = [

            rider for rider in self.squad

            if rider.id != rider_id

        ]



    def team_average_cma(self):


        if not self.squad:

            return 0



        total = sum(

            rider.current_cma

            for rider in self.squad

        )


        return round(

            total / len(self.squad),

            2

        )



    # ---------------------------------------------------------
    # Match Results
    # ---------------------------------------------------------


    def record_win(self):

        self.wins += 1

        self.points += 2



    def record_loss(self):

        self.defeats += 1



# =============================================================
# VENUE MODEL
# =============================================================


@dataclass
class Venue:


    id: int

    name: str

    location: str

    track_length: int

    capacity: int

    average_crowd: int = 0

    track_type: str = "Standard"

    home_advantage: float = 1.0



    def calculate_home_bonus(self):

        return self.home_advantage



# =============================================================
# FIXTURE MODEL
# =============================================================


@dataclass
class Fixture:


    id: int

    season: int

    round_number: int

    home_club_id: int

    away_club_id: int

    venue_id: int


    home_score: int = 0

    away_score: int = 0


    completed: bool = False



    # ---------------------------------------------------------
    # Result Processing
    # ---------------------------------------------------------


    def set_result(
            self,
            home_score: int,
            away_score: int
    ):


        self.home_score = home_score

        self.away_score = away_score

        self.completed = True



    def winner(self):


        if not self.completed:

            return None


        if self.home_score > self.away_score:

            return self.home_club_id


        if self.away_score > self.home_score:

            return self.away_club_id


        return "Draw"



# =============================================================
# DATABASE OBJECT FACTORY HELPERS
# =============================================================


def create_rider_from_json(data: Dict):


    return Rider(

        id=data.get(
            "id"
        ),

        name=data.get(
            "name",
            "Unknown"
        ),

        nationality=data.get(
            "nationality",
            "Unknown"
        ),

        age=data.get(
            "age",
            18
        ),

        historical_cma=data.get(
            "historical_cma",
            0
        ),

        current_cma=data.get(
            "current_cma",
            data.get(
                "historical_cma",
                0
            )
        ),

        potential=data.get(
            "potential",
            0
        )

    )



def create_club_from_json(data: Dict):


    return Club(

        id=data.get(
            "id"
        ),

        name=data.get(
            "name",
            "Unknown"
        ),

        location=data.get(
            "location",
            ""
        ),

        founded=data.get(
            "founded",
            1900
        ),

        stadium=data.get(
            "stadium",
            ""
        ),

        league=data.get(
            "league",
            ""

        )

    )



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    rider = Rider(

        id=1,

        name="Example Rider",

        current_cma=8.75

    )


    print(
        rider.name,
        rider.racing_ability()
    )
