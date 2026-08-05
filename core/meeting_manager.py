"""
British League Speedway Manager

Meeting Manager

Version: 0.3.3 Alpha

Controls Speedway race nights.

Responsibilities:

- Start meetings
- Connect fixtures to race engine
- Run heats
- Process results
- Update league tables
- Complete fixtures

"""


from __future__ import annotations


from dataclasses import dataclass, field
from typing import Optional, List


from core.logger import get_logger


log = get_logger(
    "MeetingManager"
)



# ==========================================================
# MEETING STATE
# ==========================================================


@dataclass
class MeetingState:


    home_team: str

    away_team: str

    date: str


    current_heat: int = 0


    total_heats: int = 15


    home_score: int = 0

    away_score: int = 0


    completed: bool = False


    heat_results: List = field(
        default_factory=list
    )



# ==========================================================
# MEETING MANAGER
# ==========================================================


class MeetingManager:


    def __init__(
        self,
        race_engine=None,
        result_processor=None,
        league_processor=None,
    ):


        self.race_engine = race_engine

        self.result_processor = result_processor

        self.league_processor = league_processor


        self.current_meeting: Optional[MeetingState] = None



    # ======================================================
    # START MEETING
    # ======================================================


    def start_meeting(
        self,
        fixture,
    ):


        self.current_meeting = MeetingState(

            home_team=fixture.home_team,

            away_team=fixture.away_team,

            date=fixture.meeting_date

        )


        log.info(

            f"Meeting started: "
            f"{fixture.home_team} v {fixture.away_team}"

        )


        return self.current_meeting



    # ======================================================
    # PROCESS HEAT
    # ======================================================


    def process_heat(
        self,
        heat_result,
    ):


        if not self.current_meeting:

            raise RuntimeError(
                "No active meeting"
            )


        self.current_meeting.current_heat += 1


        self.current_meeting.heat_results.append(
            heat_result
        )


        for rider in heat_result:

            if rider["team"] == "home":

                if rider["position"] == 1:
                    self.current_meeting.home_score += 3

                elif rider["position"] == 2:
                    self.current_meeting.home_score += 2

                elif rider["position"] == 3:
                    self.current_meeting.home_score += 1


            else:

                if rider["position"] == 1:
                    self.current_meeting.away_score += 3

                elif rider["position"] == 2:
                    self.current_meeting.away_score += 2

                elif rider["position"] == 3:
                    self.current_meeting.away_score += 1



        return self.current_meeting



    # ======================================================
    # COMPLETE MEETING
    # ======================================================


    def complete_meeting(self):


        if not self.current_meeting:

            return None



        self.current_meeting.completed = True



        log.info(

            f"Meeting completed: "
            f"{self.current_meeting.home_score}-"
            f"{self.current_meeting.away_score}"

        )


        return self.current_meeting



    # ======================================================
    # SUMMARY
    ======================================================


    def summary(self):


        if not self.current_meeting:

            return {
                "active": False
            }



        return {


            "active": True,


            "date":
                self.current_meeting.date,


            "home":
                self.current_meeting.home_team,


            "away":
                self.current_meeting.away_team,


            "heat":
                self.current_meeting.current_heat,


            "score":

                (
                    self.current_meeting.home_score,
                    self.current_meeting.away_score
                ),


            "completed":
                self.current_meeting.completed

        }



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


meeting_manager = MeetingManager()



# ==========================================================
# TEST
# ==========================================================


if __name__ == "__main__":


    print(
        "Meeting Manager V0.3.3 loaded"
    )
