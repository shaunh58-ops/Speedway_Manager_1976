"""
Speedway Game Engine

Calendar Engine Module

Version: 1.0

Controls the Speedway season timeline,
fixtures and scheduled events.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class CalendarEvent:


    event_id: int

    date: str

    event_type: str

    description: str

    completed: bool = False



@dataclass(slots=True)
class SeasonCalendar:


    year: int

    events: List[CalendarEvent] = field(

        default_factory=list

    )



# ==========================================================
# CALENDAR ENGINE
# ==========================================================


class CalendarEngine:


    def __init__(self):

        self.calendar: Optional[SeasonCalendar] = None

        self.event_counter = 1



    # ======================================================
    # CREATE SEASON
    # ======================================================


    def create_season(
            self,
            year
    ):


        self.calendar = SeasonCalendar(

            year

        )


        return self.calendar



    # ======================================================
    # ADD EVENT
    # ======================================================


    def add_event(
            self,
            date,
            event_type,
            description
    ):


        if not self.calendar:

            raise Exception(

                "Season calendar not created"

            )



        event = CalendarEvent(

            self.event_counter,

            date,

            event_type,

            description

        )


        self.calendar.events.append(

            event

        )


        self.event_counter += 1



        return event



    # ======================================================
    # ADD FIXTURE
    # ======================================================


    def add_fixture(
            self,
            date,
            home_team,
            away_team
    ):


        return self.add_event(

            date,

            "Fixture",

            f"{home_team} vs {away_team}"

        )



    # ======================================================
    # ADD CUP EVENT
    ======================================================


    def add_cup_round(
            self,
            date,
            competition,
            teams
    ):


        return self.add_event(

            date,

            "Cup",

            f"{competition}: {teams}"

        )



    # ======================================================
    # FIND EVENTS
    ======================================================


    def events_on_date(
            self,
            date
    ):


        if not self.calendar:

            return []



        return [

            event

            for event

            in self.calendar.events

            if event.date == date

        ]



    # ======================================================
    # COMPLETE EVENT
    ======================================================


    def complete_event(
            self,
            event_id
    ):


        for event in self.calendar.events:


            if event.event_id == event_id:


                event.completed = True

                return True



        return False



    # ======================================================
    # RESCHEDULE EVENT
    ======================================================


    def reschedule_event(
            self,
            event_id,
            new_date
    ):


        for event in self.calendar.events:


            if event.event_id == event_id:


                event.date = new_date

                event.completed = False

                return True



        return False



    # ======================================================
    # NEXT EVENT
    ======================================================


    def next_event(
            self,
            current_date
    ):


        future_events = [

            event

            for event

            in self.calendar.events

            if event.date > current_date

            and not event.completed

        ]


        if not future_events:

            return None



        return sorted(

            future_events,

            key=lambda x: x.date

        )[0]



    # ======================================================
    # DAILY CHECK
    ======================================================


    def process_date(
            self,
            current_date
    ):


        return self.events_on_date(

            current_date

        )



    # ======================================================
    # SUMMARY
    ======================================================


    def summary(self):


        if not self.calendar:

            return {}



        return {


            "year":

                self.calendar.year,


            "total_events":

                len(

                    self.calendar.events

                ),


            "completed":

                len(

                    [

                    e for e

                    in self.calendar.events

                    if e.completed

                    ]

                )

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    calendar = CalendarEngine()


    calendar.create_season(

        1976

    )


    calendar.add_fixture(

        "1976-04-03",

        "Belle Vue",

        "Coventry"

    )


    calendar.add_fixture(

        "1976-04-10",

        "Wolverhampton",

        "Poole"

    )


    print(

        calendar.summary()

    )
