"""
Speedway Game Engine

Calendar Manager Module

Version: 1.0

Controls the yearly Speedway calendar,
events and season progression.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class CalendarEvent:


    event_id: int

    name: str

    event_type: str

    event_date: date

    completed: bool = False

    notes: str = ""



@dataclass(slots=True)
class SeasonCalendar:


    season: int

    start_date: date

    end_date: date

    events: List[CalendarEvent] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class CalendarManager:


    def __init__(self):

        self.calendars: Dict[int, SeasonCalendar] = {}

        self.next_event_id = 1



    # ======================================================
    # CREATE SEASON
    # ======================================================


    def create_season(
            self,
            season,
            start_month=3,
            start_day=1
    ):


        start = date(

            season,

            start_month,

            start_day

        )


        end = date(

            season,

            11,

            30

        )


        calendar = SeasonCalendar(

            season=season,

            start_date=start,

            end_date=end

        )


        self.calendars[season] = calendar


        return calendar



    # ======================================================
    # ADD EVENT
    # ======================================================


    def add_event(
            self,
            season,
            name,
            event_type,
            event_date,
            notes=""
    ):


        calendar = self.calendars.get(

            season

        )


        if not calendar:

            return None



        event = CalendarEvent(

            event_id=self.next_event_id,

            name=name,

            event_type=event_type,

            event_date=event_date,

            notes=notes

        )


        calendar.events.append(

            event

        )


        self.next_event_id += 1


        return event



    # ======================================================
    # GENERATE STANDARD SEASON
    # ======================================================


    def generate_speedway_season(
            self,
            season
    ):


        if season not in self.calendars:

            self.create_season(

                season

            )


        calendar = self.calendars[season]


        self.add_event(

            season,

            "Pre Season Training",

            "Training",

            date(

                season,

                3,

                1

            )

        )


        self.add_event(

            season,

            "League Opening Night",

            "League",

            date(

                season,

                4,

                1

            )

        )


        self.add_event(

            season,

            "Transfer Window Opens",

            "Transfer",

            date(

                season,

                11,

                1

            )

        )


        self.add_event(

            season,

            "Season Awards",

            "Awards",

            date(

                season,

                10,

                15

            )

        )


        return calendar



    # ======================================================
    # ADVANCE TIME
    # ======================================================


    def advance_day(
            self,
            current_date
    ):


        return current_date + timedelta(

            days=1

        )



    # ======================================================
    # UPCOMING EVENTS
    # ======================================================


    def upcoming_events(
            self,
            season,
            current_date
    ):


        calendar = self.calendars.get(

            season

        )


        if not calendar:

            return []



        return [

            event

            for event

            in calendar.events

            if event.event_date >= current_date

            and not event.completed

        ]



    # ======================================================
    # COMPLETE EVENT
    ======================================================


    def complete_event(
            self,
            season,
            event_id
    ):


        calendar = self.calendars[season]


        for event in calendar.events:


            if event.event_id == event_id:


                event.completed = True


                return True



        return False



    # ======================================================
    # SEASON PHASE
    # ======================================================


    def season_phase(
            self,
            current_date
    ):


        month = current_date.month


        if month <= 3:

            return "Pre Season"


        if month <= 9:

            return "Competitive Season"


        return "Off Season"



    # ======================================================
    # REPORT
    # ======================================================


    def calendar_report(
            self,
            season
    ):


        calendar = self.calendars.get(

            season

        )


        if not calendar:

            return None



        return {


            "season":

                calendar.season,


            "start":

                calendar.start_date,


            "end":

                calendar.end_date,


            "events":

                len(calendar.events)

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = CalendarManager()


    manager.generate_speedway_season(

        1976

    )


    print(

        manager.calendar_report(

            1976

        )

    )
