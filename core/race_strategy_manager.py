"""
Speedway Game Engine

Race Strategy Manager Module

Version: 1.0

Controls tactical decisions,
rider selection and race strategies.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class TeamStrategy:


    team_id: int

    manager_style: str

    preferred_riders: List[int] = field(
        default_factory=list
    )

    aggressive_level: int = 50

    risk_level: int = 50



@dataclass(slots=True)
class HeatDecision:


    heat_number: int

    riders_selected: List[int]

    tactic: str

    confidence: int



# ==========================================================
# MANAGER
# ==========================================================


class RaceStrategyManager:


    def __init__(self):

        self.strategies: Dict[int, TeamStrategy] = {}

        self.decisions: List[HeatDecision] = []



    # ======================================================
    # CREATE TEAM STRATEGY
    # ======================================================


    def create_strategy(
            self,
            team_id,
            manager_style="Balanced"
    ):


        strategy = TeamStrategy(

            team_id=team_id,

            manager_style=manager_style

        )


        if manager_style == "Aggressive":

            strategy.aggressive_level = 80

            strategy.risk_level = 80



        elif manager_style == "Conservative":

            strategy.aggressive_level = 30

            strategy.risk_level = 20



        else:

            strategy.aggressive_level = 50

            strategy.risk_level = 50



        self.strategies[team_id] = strategy


        return strategy



    # ======================================================
    # SELECT RIDERS
    # ======================================================


    def select_heat_riders(
            self,
            team_id,
            available_riders,
            heat_number
    ):


        strategy = self.strategies[team_id]


        riders = available_riders.copy()



        # Prefer experienced riders late in meetings

        if heat_number >= 13:


            riders.sort(

                key=lambda r:

                getattr(

                    r,

                    "experience",

                    0

                ),

                reverse=True

            )



        else:


            random.shuffle(

                riders

            )



        selected = riders[:2]



        decision = HeatDecision(

            heat_number=heat_number,

            riders_selected=selected,

            tactic="Standard",

            confidence=random.randint(

                50,

                90

            )

        )


        self.decisions.append(

            decision

        )


        return selected



    # ======================================================
    # TACTICAL SUBSTITUTE
    # ======================================================


    def tactical_substitute(
            self,
            team_id,
            rider,
            score_difference
    ):


        strategy = self.strategies[team_id]



        if score_difference < -8:


            if strategy.risk_level > 60:


                return True



        return False



    # ======================================================
    # RIDER PAIRING SCORE
    # ======================================================


    def pairing_score(
            self,
            rider_one,
            rider_two
    ):


        score = 0



        score += getattr(

            rider_one,

            "consistency",

            50

        )



        score += getattr(

            rider_two,

            "consistency",

            50

        )



        return score / 2



    # ======================================================
    # MATCH APPROACH
    # ======================================================


    def match_plan(
            self,
            team_id,
            opponent_strength
    ):


        strategy = self.strategies[team_id]


        if opponent_strength > 80:


            if strategy.aggressive_level > 60:

                return "Attack Early"


            return "Control Damage"



        return "Build Lead"



    # ======================================================
    # REPORT
    # ======================================================


    def strategy_report(
            self,
            team_id
    ):


        strategy = self.strategies.get(

            team_id

        )


        if not strategy:

            return None



        return {


            "style":

                strategy.manager_style,


            "aggression":

                strategy.aggressive_level,


            "risk":

                strategy.risk_level

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = RaceStrategyManager()


    manager.create_strategy(

        1,

        "Aggressive"

    )


    print(

        manager.strategy_report(

            1

        )

    )
