"""
Speedway Game Engine

Championship Calendar Manager Module

Version: 1.0

Controls major championship events,
qualification stages and finals.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class ChampionshipEvent:


    event_id: int

    name: str

    category: str

    event_date: date

    stage: str

    completed: bool = False

    winner_id: int | None = None



@dataclass(slots=True)
class ChampionshipSeason:


    season: int

    championship_name: str

    events: List[ChampionshipEvent] = field(
        default_factory=list
    )

    champion_id: int | None = None



# ==========================================================
# MANAGER
# ==========================================================


class ChampionshipCalendarManager:


    def __init__(self):

        self.championships: Dict[str, ChampionshipSeason] = {}

        self.next_event_id = 1



    # ======================================================
    # CREATE CHAMPIONSHIP
    # ======================================================


    def create_championship(
            self,
            season,
            name
    ):


        championship = ChampionshipSeason(

            season=season,

            championship_name=name

        )


        key = f"{season}_{name}"


        self.championships[key] = championship


        return championship



    # ======================================================
    # ADD EVENT
    ======================================================


    def add_event(
            self,
            season,
            championship_name,
            name,
            category,
            event_date,
            stage
    ):


        key = f"{season}_{championship_name}"


        championship = self.championships.get(

            key

        )


        if not championship:

            return None



        event = ChampionshipEvent(

            event_id=self.next_event_id,

            name=name,

            category=category,

            event_date=event_date,

            stage=stage

        )


        championship.events.append(

            event

        )


        self.next_event_id += 1


        return event



    # ======================================================
    # GENERATE HISTORICAL STRUCTURE
    ======================================================


    def generate_world_championship(
            self,
            season
    ):


        name = "World Individual Championship"


        self.create_championship(

            season,

            name

        )


        # Historical format example

        self.add_event(

            season,

            name,

            "British Qualifying Round",

            "Qualification",

            date(

                season,

                4,

                15

            ),

            "Round 1"

        )


        self.add_event(

            season,

            name,

            "British Final",

            "Qualification",

            date(

                season,

                5,

                30

            ),

            "National Final"

        )


        self.add_event(

            season,

            name,

            "World Final",

            "Final",

            date(

                season,

                9,

                20

            ),

            "World Final"

        )


        return self.championships[

            f"{season}_{name}"

        ]



    # ======================================================
    # COMPLETE EVENT
    ======================================================


    def complete_event(
            self,
            season,
            championship_name,
            event_id,
            winner_id
    ):


        key = f"{season}_{championship_name}"


        championship = self.championships[key]


        for event in championship.events:


            if event.event_id == event_id:


                event.completed = True

                event.winner_id = winner_id


                return True



        return False



    # ======================================================
    # SET CHAMPION
    ======================================================


    def declare_champion(
            self,
            season,
            championship_name,
            rider_id
    ):


        key = f"{season}_{championship_name}"


        championship = self.championships[key]


        championship.champion_id = rider_id


        return rider_id



    # ======================================================
    # UPCOMING EVENTS
    ======================================================


    def upcoming_events(
            self,
            season,
            championship_name,
            current_date
    ):


        key = f"{season}_{championship_name}"


        championship = self.championships.get(

            key

        )


        if not championship:

            return []



        return [

            event

            for event

            in championship.events

            if event.event_date >= current_date

            and not event.completed

        ]



    # ======================================================
    # REPORT
    ======================================================


    def championship_report(
            self,
            season,
            championship_name
    ):


        key = f"{season}_{championship_name}"


        championship = self.championships.get(

            key

        )


        if not championship:

            return None



        return {


            "season":

                championship.season,


            "competition":

                championship.championship_name,


            "events":

                len(

                    championship.events

                ),


            "champion":

                championship.champion_id

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = ChampionshipCalendarManager()


    manager.generate_world_championship(

        1976

    )


    print(

        manager.championship_report(

            1976,

            "World Individual Championship"

        )

    )
