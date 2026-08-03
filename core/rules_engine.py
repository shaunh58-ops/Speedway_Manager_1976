"""
Speedway Game Engine

Rules Engine Module

Version: 1.0

Controls Speedway competition rules.

Features:

- Heat formats
- Scoring systems
- Match points
- Tactical substitutions
- Rider replacement
- Competition rules

"""


from typing import Dict, List



class RulesEngine:



    def __init__(
            self,
            rule_set="British League 1976"
    ):


        self.rule_set = rule_set


        self.rules = self.load_rules()



    # =========================================================
    # RULE DATABASE
    # =========================================================


    def load_rules(self):


        rule_database = {



            "British League 1976":
            {


                "heats":

                    13,


                "riders_per_heat":

                    4,


                "points":

                    {

                    "1st":3,

                    "2nd":2,

                    "3rd":1,

                    "4th":0

                    },


                "home_win_points":

                    2,


                "away_win_points":

                    2,


                "draw_points":

                    1,


                "tactical_substitute":

                    True,


                "reserve_replacement":

                    True

            },



            "Modern Speedway":
            {


                "heats":

                    15,


                "riders_per_heat":

                    4,


                "points":

                    {

                    "1st":3,

                    "2nd":2,

                    "3rd":1,

                    "4th":0

                    },


                "tactical_substitute":

                    True,


                "reserve_replacement":

                    True

            }


        }



        return rule_database.get(

            self.rule_set,

            rule_database["British League 1976"]

        )



    # =========================================================
    # HEAT MANAGEMENT
    # =========================================================


    def total_heats(self):

        return self.rules["heats"]



    def riders_per_heat(self):

        return self.rules["riders_per_heat"]



    def heat_points(
            self,
            finishing_position
    ):


        scoring = [

            3,

            2,

            1,

            0

        ]


        if finishing_position <= 4:


            return scoring[
                finishing_position - 1
            ]



        return 0



    # =========================================================
    # MATCH SCORING
    # =========================================================


    def calculate_match_points(
            self,
            home_score,
            away_score
    ):


        if home_score > away_score:


            return {


                "home":

                    self.rules.get(

                        "home_win_points",

                        2

                    ),


                "away":

                    0

            }



        elif away_score > home_score:


            return {


                "home":

                    0,


                "away":

                    self.rules.get(

                        "away_win_points",

                        2

                    )

            }



        else:


            return {


                "home":

                    self.rules.get(

                        "draw_points",

                        1

                    ),


                "away":

                    self.rules.get(

                        "draw_points",

                        1

                    )

            }



    # =========================================================
    # TACTICAL SUBSTITUTE SYSTEM
    # =========================================================


    def can_use_tactical_substitute(
            self,
            team_score,
            opponent_score
    ):


        if not self.rules.get(

            "tactical_substitute",

            False

        ):

            return False



        deficit = opponent_score - team_score



        return deficit >= 6



    # =========================================================
    # RIDER REPLACEMENT
    # =========================================================


    def eligible_replacement(
            self,
            rider
    ):


        if not self.rules.get(

            "reserve_replacement",

            False

        ):

            return False



        return (

            rider.injuries > 0

            or

            rider.retired

        )



    # =========================================================
    # MEETING VALIDATION
    # =========================================================


    def validate_meeting(
            self,
            home_team,
            away_team
    ):


        errors = []



        if len(home_team.squad) < 7:


            errors.append(

                "Home team has insufficient riders"

            )



        if len(away_team.squad) < 7:


            errors.append(

                "Away team has insufficient riders"

            )



        return {


            "valid":

                len(errors) == 0,


            "errors":

                errors

        }



    # =========================================================
    # RULE SUMMARY
    # =========================================================


    def summary(self):


        return {


            "rule_set":

                self.rule_set,


            "heats":

                self.rules["heats"],


            "riders_per_heat":

                self.rules["riders_per_heat"],


            "tactical_substitutions":

                self.rules.get(

                    "tactical_substitute",

                    False

                )

        }



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    rules = RulesEngine()



    print(

        rules.summary()

    )
