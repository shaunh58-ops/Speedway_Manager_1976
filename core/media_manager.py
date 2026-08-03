"""
Speedway Game Engine

Media Manager Module

Version: 1.0

Controls media coverage, popularity and public reputation.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class MediaEvent:


    season: int

    headline: str

    category: str

    impact: int



@dataclass(slots=True)
class PublicProfile:


    entity_id: int

    popularity: int = 50

    reputation: int = 50

    media_attention: int = 0

    history: List[MediaEvent] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class MediaManager:


    def __init__(self):


        self.rider_profiles: Dict[int, PublicProfile] = {}

        self.club_profiles: Dict[int, PublicProfile] = {}

        self.media_history: List[MediaEvent] = []



    # ======================================================
    # PROFILE MANAGEMENT
    # ======================================================


    def get_rider_profile(
            self,
            rider_id
    ):


        if rider_id not in self.rider_profiles:


            self.rider_profiles[rider_id] = PublicProfile(

                entity_id=rider_id

            )


        return self.rider_profiles[rider_id]



    def get_club_profile(
            self,
            club_id
    ):


        if club_id not in self.club_profiles:


            self.club_profiles[club_id] = PublicProfile(

                entity_id=club_id

            )


        return self.club_profiles[club_id]



    # ======================================================
    # CREATE MEDIA EVENT
    # ======================================================


    def create_story(
            self,
            entity_type,
            entity_id,
            season,
            headline,
            category,
            impact
    ):


        event = MediaEvent(

            season=season,

            headline=headline,

            category=category,

            impact=impact

        )


        self.media_history.append(

            event

        )


        if entity_type == "rider":


            profile = self.get_rider_profile(

                entity_id

            )


        else:


            profile = self.get_club_profile(

                entity_id

            )



        profile.history.append(

            event

        )


        profile.media_attention += impact


        profile.popularity += impact


        profile.reputation += impact



        self.clamp_profile(

            profile

        )


        return event



    # ======================================================
    # AUTOMATIC STORIES
    # ======================================================


    def race_result_story(
            self,
            rider,
            position,
            season
    ):


        if position == 1:


            headline = (

                f"{rider.name} dominates Speedway meeting"

            )


            impact = 5



        elif position <= 3:


            headline = (

                f"{rider.name} claims podium finish"

            )


            impact = 2



        else:


            headline = (

                f"{rider.name} struggles for form"

            )


            impact = -1



        return self.create_story(

            "rider",

            rider.id,

            season,

            headline,

            "Race Result",

            impact

        )



    # ======================================================
    # CHAMPIONSHIP STORIES
    # ======================================================


    def championship_story(
            self,
            entity,
            season,
            champion=True
    ):


        if champion:


            headline = (

                f"{entity.name} crowned Speedway Champion"

            )


            impact = 15



        else:


            headline = (

                f"{entity.name} misses championship glory"

            )


            impact = -3



        entity_type = (

            "club"

            if hasattr(entity, "club_id")

            else

            "rider"

        )



        return self.create_story(

            entity_type,

            entity.id,

            season,

            headline,

            "Championship",

            impact

        )



    # ======================================================
    # RIVALRIES
    # ======================================================


    def create_rivalry_story(
            self,
            club_a,
            club_b,
            season
    ):


        headline = (

            f"{club_a.name} and {club_b.name} rivalry intensifies"

        )


        event = MediaEvent(

            season=season,

            headline=headline,

            category="Rivalry",

            impact=10

        )


        self.media_history.append(

            event

        )


        return event



    # ======================================================
    # ERA EFFECT
    # ======================================================


    def media_multiplier(
            self,
            year
    ):


        if year < 1985:

            return 1.0


        if year < 2000:

            return 1.25


        return 1.75



    # ======================================================
    # PROFILE CONTROL
    # ======================================================


    def clamp_profile(
            self,
            profile
    ):


        profile.popularity = max(

            0,

            min(

                100,

                profile.popularity

            )

        )


        profile.reputation = max(

            0,

            min(

                100,

                profile.reputation

            )

        )



    # ======================================================
    # REPORTS
    # ======================================================


    def top_media_figures(
            self
    ):


        riders = sorted(

            self.rider_profiles.values(),

            key=lambda x:

            x.popularity,

            reverse=True

        )


        clubs = sorted(

            self.club_profiles.values(),

            key=lambda x:

            x.popularity,

            reverse=True

        )


        return {


            "riders":

                riders[:10],


            "clubs":

                clubs[:10]

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = MediaManager()


    print(

        "Media Manager Loaded"

    )
