"""
British League Speedway Manager
Club Database Manager
Version: 1.0

Designed specifically for the Historical Club Database v1.1
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from core.logger import get_logger

log = get_logger("ClubDatabaseManager")


HOME_ADVANTAGE = {
    "Very High": 1.08,
    "High": 1.05,
    "Medium-High": 1.035,
    "Medium": 1.02,
    "Low-Medium": 1.01,
    "Low": 1.00,
}


@dataclass
class Club:

    club_id: str

    name: str

    nickname: str

    stadium: str

    stadium_capacity: int

    average_attendance: int

    track_size: int

    race_night: str

    home_advantage_text: str

    home_advantage: float

    starting_bank_balance: int

    board_expectations: str

    fan_loyalty: str

    rivals: List[str] = field(default_factory=list)

    riders: List[str] = field(default_factory=list)


class ClubDatabaseManager:

    def __init__(self, database_path=None):

        self.database_path = database_path

        self.clubs: Dict[str, Club] = {}

    def load_database(self, file_path=None):

        path = Path(file_path or self.database_path)

        if not path.exists():
            raise FileNotFoundError(path)

        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)

        self.clubs.clear()

        for record in records:

            club = self.create_club(record)

            self.clubs[club.club_id] = club

        log.info("Loaded %s clubs", len(self.clubs))

        return self.clubs

    def create_club(self, data):

        track = self._parse_int(data.get("Track Size.", 0))

        capacity = self._parse_int(data.get("Stadium Capacity.", 0))

        attendance = self._parse_int(data.get("Average Attendance.", 0))

        balance = self._parse_money(data.get("Starting Bank Balance.", 0))

        rivals = self._parse_rivals(data.get("Rivals", ""))

        modifier_text = data.get("Home Advantage Modifier.", "Medium")

        return Club(

            club_id=str(data.get("ID No.", "")),

            name=data.get("Club", ""),

            nickname=data.get("Nickname", ""),

            stadium=data.get("Stadium", ""),

            stadium_capacity=capacity,

            average_attendance=attendance,

            track_size=track,

            race_night=data.get("Race Night", ""),

            home_advantage_text=modifier_text,

            home_advantage=HOME_ADVANTAGE.get(
                modifier_text,
                1.02
            ),

            starting_bank_balance=balance,

            board_expectations=data.get(
                "Board Expectations.",
                ""
            ),

            fan_loyalty=data.get(
                "Fan Loyalty.",
                ""
            ),

            rivals=rivals,

        )

    def get_club(self, club_id):

        return self.clubs.get(str(club_id))

    def get_club_by_name(self, name):

        for club in self.clubs.values():

            if club.name.lower() == name.lower():

                return club

        return None

    def get_active_clubs(self):

        return sorted(

            self.clubs.values(),

            key=lambda c: c.name

        )

    def assign_riders(self, rider_database):

        for club in self.clubs.values():

            club.riders = []

        for rider in rider_database.values():

            club = self.get_club_by_name(rider.club)

            if club:

                club.riders.append(rider.rider_id)

    @staticmethod
    def _parse_int(value):

        if value is None:
            return 0

        value = str(value)

        digits = re.sub(r"[^\d]", "", value)

        return int(digits) if digits else 0

    @staticmethod
    def _parse_money(value):

        return ClubDatabaseManager._parse_int(value)

    @staticmethod
    def _parse_rivals(value):

        if not value:
            return []

        if isinstance(value, list):
            return value

        return [
            rival.strip()
            for rival in str(value).split(",")
            if rival.strip()
        ]


club_database_manager = ClubDatabaseManager()
