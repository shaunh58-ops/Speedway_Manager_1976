"""
British League Speedway Manager

Result Processor

Version: Alpha 0.1

Processes completed heats and meetings.
"""


from __future__ import annotations


from dataclasses import dataclass, field


from typing import Dict, List



from core.logger import get_logger


from core.event_bus import event_bus



log = get_logger(

    "ResultProcessor"

)



# ==========================================================
# MEETING RESULT
# ==========================================================


@dataclass
class MeetingResult:


    home_team: str


    away_team: str


    home_points: int = 0


    away_points: int = 0


    heats: List = field(

        default_factory=list

    )



# ==========================================================
# RESULT PROCESSOR
# ==========================================================


class ResultProcessor:


    def __init__(self):


        self.current_meeting = None


        self.rider_statistics = {}



    # ======================================================
    # START MEETING
    ======================================================


    def start_meeting(
        self,
        home_team,
        away_team,
    ):


        self.current_meeting = MeetingResult(

            home_team=home_team,

            away_team=away_team

        )



        log.info(

            f"Meeting started: {home_team} vs {away_team}"

        )



    # ======================================================
    # PROCESS HEAT
    ======================================================


    def process_heat(
        self,
        heat_result,
    ):


        if not self.current_meeting:


            raise RuntimeError(

                "No active meeting"

            )



        self.current_meeting.heats.append(

            heat_result

        )



        for rider in heat_result:


            self.update_rider_statistics(

                rider

            )


        self.update_team_score(

            heat_result

        )



        event_bus.publish(

            "heat_processed",

            result=heat_result

        )



    # ======================================================
    # TEAM SCORING
    ======================================================


    def update_team_score(
        self,
        heat_result,
    ):


        for rider in heat_result:



            if rider.finishing_position == 1:


                points = rider.points


            else:


                points = rider.points



            # Future:
            # determine rider team here


    # ======================================================
    # RIDER STATISTICS
    ======================================================


    def update_rider_statistics(
        self,
        rider_result,
    ):


        rider_id = rider_result.rider_id



        if rider_id not in self.rider_statistics:


            self.rider_statistics[rider_id] = {


                "rides":0,

                "points":0,

                "wins":0

            }



        stats = self.rider_statistics[rider_id]



        stats["rides"] += 1


        stats["points"] += rider_result.points



        if rider_result.finishing_position == 1:


            stats["wins"] += 1



    # ======================================================
    # COMPLETE MEETING
    ======================================================


    def finish_meeting(self):


        if not self.current_meeting:


            return None



        result = self.current_meeting



        event_bus.publish(

            "meeting_completed",

            result=result

        )



        log.info(

            "Meeting completed"

        )



        self.current_meeting = None



        return result



    # ======================================================
    # STATISTICS ACCESS
    ======================================================


    def get_rider_statistics(self):


        return self.rider_statistics



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


result_processor = ResultProcessor()
