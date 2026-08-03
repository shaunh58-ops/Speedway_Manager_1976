"""
Speedway Game Engine

Statistics Manager

Version: 1.0

Central statistics repository.

All completed races, meetings and seasons should
ultimately update this module.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


# ==========================================================
# DATA CLASSES
# ==========================================================

@dataclass(slots=True)
class RiderStatistics:

    rider_id: int

    meetings: int = 0

    heats: int = 0

    rides: int = 0

    wins: int = 0

    second_places: int = 0

    third_places: int = 0

    fourth_places: int = 0

    points: int = 0

    bonus_points: int = 0

    exclusions: int = 0

    falls: int = 0

    retirements: int = 0

    average: float = 0.0


@dataclass(slots=True)
class ClubStatistics:

    club_id: int

    meetings: int = 0

    wins: int = 0

    draws: int = 0

    losses: int = 0

    points_for: int = 0

    points_against: int = 0

    league_points: int = 0


# ==========================================================
# MANAGER
# ==========================================================

class StatisticsManager:

    def __init__(self):

        self.riders: Dict[int, RiderStatistics] = {}

        self.clubs: Dict[int, ClubStatistics] = {}

        self.championship_history: List[dict] = []

        self.match_history: List[dict] = []

    # ======================================================
    # RIDERS
    # ======================================================

    def rider_stats(
        self,
        rider_id: int
    ) -> RiderStatistics:

        if rider_id not in self.riders:

            self.riders[rider_id] = RiderStatistics(

                rider_id=rider_id

            )

        return self.riders[rider_id]

    def record_heat(
        self,
        rider_id: int,
        finishing_position: int,
        points: int,
        bonus: int = 0
    ):

        stats = self.rider_stats(rider_id)

        stats.heats += 1

        stats.rides += 1

        stats.points += points

        stats.bonus_points += bonus

        if finishing_position == 1:
            stats.wins += 1

        elif finishing_position == 2:
            stats.second_places += 1

        elif finishing_position == 3:
            stats.third_places += 1

        else:
            stats.fourth_places += 1

        stats.average = round(

            stats.points /

            max(stats.rides, 1),

            2

        )

    def record_meeting(
        self,
        rider_id: int
    ):

        self.rider_stats(

            rider_id

        ).meetings += 1

    # ======================================================
    # CLUBS
    # ======================================================

    def club_stats(
        self,
        club_id: int
    ) -> ClubStatistics:

        if club_id not in self.clubs:

            self.clubs[club_id] = ClubStatistics(

                club_id=club_id

            )

        return self.clubs[club_id]

    def record_match(
        self,
        home_id: int,
        away_id: int,
        home_score: int,
        away_score: int
    ):

        home = self.club_stats(home_id)

        away = self.club_stats(away_id)

        home.meetings += 1

        away.meetings += 1

        home.points_for += home_score

        home.points_against += away_score

        away.points_for += away_score

        away.points_against += home_score

        if home_score > away_score:

            home.wins += 1

            away.losses += 1

            home.league_points += 2

        elif away_score > home_score:

            away.wins += 1

            home.losses += 1

            away.league_points += 2

        else:

            home.draws += 1

            away.draws += 1

            home.league_points += 1

            away.league_points += 1

        self.match_history.append({

            "home": home_id,

            "away": away_id,

            "home_score": home_score,

            "away_score": away_score

        })

    # ======================================================
    # CHAMPIONSHIPS
    # ======================================================

    def record_champion(
        self,
        season: int,
        club_name: str
    ):

        self.championship_history.append({

            "season": season,

            "champion": club_name

        })

    # ======================================================
    # LEADERBOARDS
    # ======================================================

    def top_riders(
        self,
        limit: int = 10
    ):

        return sorted(

            self.riders.values(),

            key=lambda r: (

                r.average,

                r.points

            ),

            reverse=True

        )[:limit]

    def league_table(self):

        return sorted(

            self.clubs.values(),

            key=lambda c: (

                c.league_points,

                c.points_for -

                c.points_against

            ),

            reverse=True

        )

    # ======================================================
    # SUMMARY
    # ======================================================

    def summary(self):

        return {

            "riders":

                len(self.riders),

            "clubs":

                len(self.clubs),

            "matches":

                len(self.match_history),

            "championships":

                len(self.championship_history)

        }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    stats = StatisticsManager()

    stats.record_heat(

        rider_id=1,

        finishing_position=1,

        points=3

    )

    stats.record_match(

        1,

        2,

        46,

        32

    )

    print(

        stats.summary()

    )
