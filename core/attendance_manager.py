"""
Speedway Game Engine

Attendance Manager Module

Version: 1.0

Controls crowd behaviour, attendance trends
and supporter loyalty.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import random



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class AttendanceRecord:

    season: int

    fixture_id: int

    club_id: int

    attendance: int

    capacity: int



@dataclass(slots=True)
class FanBase:


    club_id: int

    loyalty: int = 50

    popularity: int = 50

    average_attendance: int = 0

    records: List[AttendanceRecord] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class AttendanceManager:


    def __init__(self):

        self.fans: Dict[int, FanBase] = {}

        self.history: List[AttendanceRecord] = []



    # ======================================================
    # FAN BASE
    # ======================================================


    def get_fanbase(
            self,
            club_id
    ):


        if club_id not in self.fans:


            self.fans[club_id] = FanBase(

                club_id=club_id

            )


        return self.fans[club_id]



    # ======================================================
    # ATTENDANCE CALCULATION
    # ======================================================


    def calculate_attendance(
            self,
            stadium,
            club,
            opponent,
            weather,
            importance=50
    ):


        fanbase = self.get_fanbase(

            club.id

        )


        attendance = stadium.capacity * 0.35



        # Club reputation

        attendance += (

            stadium.reputation *

            stadium.capacity *

            0.002

        )



        # Fan loyalty

        attendance += (

            fanbase.loyalty *

            stadium.capacity *

            0.003

        )



        # League importance

        attendance += (

            importance *

            stadium.capacity *

            0.003

        )



        # Rival attraction

        if getattr(

            opponent,

            "rival",

            False

        ):


            attendance += (

                stadium.capacity *

                0.15

            )



        # Weather impact


        if weather.weather.value in (

            "Heavy Rain",

            "Storm"

        ):


            attendance *= 0.65



        elif weather.weather.value == "Light Rain":


            attendance *= 0.85



        # Random variation


        attendance *= random.uniform(

            0.90,

            1.10

        )


        return min(

            int(attendance),

            stadium.capacity

        )



    # ======================================================
    # RECORD MATCH
    # ======================================================


    def record_attendance(
            self,
            season,
            fixture_id,
            club_id,
            attendance,
            capacity
    ):


        record = AttendanceRecord(

            season=season,

            fixture_id=fixture_id,

            club_id=club_id,

            attendance=attendance,

            capacity=capacity

        )


        self.history.append(

            record

        )


        fanbase = self.get_fanbase(

            club_id

        )


        fanbase.records.append(

            record

        )


        self.update_average(

            fanbase

        )


        return record



    # ======================================================
    # FAN DEVELOPMENT
    # ======================================================


    def update_fanbase(
            self,
            club_id,
            result
    ):


        fanbase = self.get_fanbase(

            club_id

        )


        if result == "win":


            fanbase.loyalty += 2



        elif result == "loss":


            fanbase.loyalty -= 1



        fanbase.loyalty = max(

            0,

            min(

                100,

                fanbase.loyalty

            )

        )



    # ======================================================
    # AVERAGES
    # ======================================================


    def update_average(
            self,
            fanbase
    ):


        if not fanbase.records:

            return



        total = sum(

            r.attendance

            for r

            in fanbase.records

        )


        fanbase.average_attendance = int(

            total /

            len(fanbase.records)

        )



    # ======================================================
    # SEASON REPORT
    # ======================================================


    def season_average(
            self,
            club_id,
            season
    ):


        records = [

            r

            for r

            in self.history

            if r.club_id == club_id

            and r.season == season

        ]



        if not records:

            return 0



        return int(

            sum(

                r.attendance

                for r

                in records

            )

            /

            len(records)

        )



    # ======================================================
    # RECORD CROWD
    # ======================================================


    def largest_crowd(
            self
    ):


        if not self.history:

            return None



        return max(

            self.history,

            key=lambda x:

            x.attendance

        )



    # ======================================================
    # REPORT
    # ======================================================


    def club_report(
            self,
            club_id
    ):


        fanbase = self.get_fanbase(

            club_id

        )


        return {


            "loyalty":

                fanbase.loyalty,


            "average":

                fanbase.average_attendance,


            "matches":

                len(fanbase.records)

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = AttendanceManager()


    print(

        "Attendance Manager Loaded"

    )
