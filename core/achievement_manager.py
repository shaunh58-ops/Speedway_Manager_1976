"""
Speedway Game Engine

Achievement Manager Module

Version: 1.0

Controls career milestones, awards and achievements.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(slots=True)
class Achievement:

    name: str

    description: str

    category: str

    season: int



class AchievementManager:


    def __init__(self):

        self.rider_achievements: Dict[int, List[Achievement]] = {}

        self.club_achievements: Dict[int, List[Achievement]] = {}

        self.manager_achievements: Dict[int, List[Achievement]] = {}


    # ======================================================
    # INTERNAL STORAGE
    # ======================================================


    def _add(
        self,
        collection,
        entity_id,
        achievement
    ):

        if entity_id not in collection:

            collection[entity_id] = []

        collection[entity_id].append(

            achievement

        )


    # ======================================================
    # RIDER ACHIEVEMENTS
    # ======================================================


    def award_rider(
        self,
        rider,
        name,
        description,
        category,
        season
    ):

        achievement = Achievement(

            name=name,

            description=description,

            category=category,

            season=season

        )

        self._add(

            self.rider_achievements,

            rider.id,

            achievement

        )

        return achievement



    def check_rider_milestones(
        self,
        rider,
        season
    ):


        awards = []


        career_wins = getattr(

            rider,

            "career_wins",

            0

        )


        championships = getattr(

            rider,

            "championships",

            0

        )


        if career_wins >= 100:


            awards.append(

                self.award_rider(

                    rider,

                    "Century Winner",

                    "Reached 100 career race victories.",

                    "Performance",

                    season

                )

            )


        if championships >= 5:


            awards.append(

                self.award_rider(

                    rider,

                    "Speedway Legend",

                    "Won five major championships.",

                    "Legacy",

                    season

                )

            )


        if getattr(

            rider,

            "world_titles",

            0

        ) >= 1:


            awards.append(

                self.award_rider(

                    rider,

                    "World Champion",

                    "Became Speedway World Champion.",

                    "Championship",

                    season

                )

            )


        return awards



    # ======================================================
    # CLUB ACHIEVEMENTS
    # ======================================================


    def award_club(
        self,
        club,
        name,
        description,
        category,
        season
    ):


        achievement = Achievement(

            name=name,

            description=description,

            category=category,

            season=season

        )


        self._add(

            self.club_achievements,

            club.id,

            achievement

        )


        return achievement



    def check_club_milestones(
        self,
        club,
        season
    ):


        awards = []


        titles = getattr(

            club,

            "league_titles",

            0

        )


        if titles >= 10:


            awards.append(

                self.award_club(

                    club,

                    "Dynasty Club",

                    "Won ten league championships.",

                    "Legacy",

                    season

                )

            )


        if titles >= 1:


            awards.append(

                self.award_club(

                    club,

                    "League Champions",

                    "Won a league championship.",

                    "Championship",

                    season

                )

            )


        return awards



    # ======================================================
    # MANAGER ACHIEVEMENTS
    # ======================================================


    def award_manager(
        self,
        manager_id,
        name,
        description,
        season
    ):


        achievement = Achievement(

            name=name,

            description=description,

            category="Manager",

            season=season

        )


        self._add(

            self.manager_achievements,

            manager_id,

            achievement

        )


        return achievement



    # ======================================================
    # REPORTS
    # ======================================================


    def rider_history(
        self,
        rider_id
    ):


        return self.rider_achievements.get(

            rider_id,

            []

        )



    def club_history(
        self,
        club_id
    ):


        return self.club_achievements.get(

            club_id,

            []

        )



    def manager_history(
        self,
        manager_id
    ):


        return self.manager_achievements.get(

            manager_id,

            []

        )



    # ======================================================
    # HALL OF FAME
    # ======================================================


    def hall_of_fame_candidates(self):


        candidates = []


        for rider_id, achievements in self.rider_achievements.items():


            score = len(achievements)


            if score >= 5:


                candidates.append(

                    rider_id

                )


        return candidates



    # ======================================================
    # SUMMARY
    # ======================================================


    def summary(self):


        return {

            "rider_awards":

                sum(

                    len(v)

                    for v

                    in self.rider_achievements.values()

                ),


            "club_awards":

                sum(

                    len(v)

                    for v

                    in self.club_achievements.values()

                ),


            "manager_awards":

                sum(

                    len(v)

                    for v

                    in self.manager_achievements.values()

                )

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = AchievementManager()


    print(

        manager.summary()

    )
