"""
British League Speedway Manager

Game State Manager

Version: 0.3.2

Controls the active game state using the historical SpeedwayWorld
created by WorldBuilder.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class CareerState:
    """Manager career information."""

    manager_name: str = ""
    club_id: Optional[str] = None
    reputation: int = 50
    career_years: int = 0


@dataclass(slots=True)
class ChampionshipState:
    """Current championship information."""

    current_competition: str = "British League"
    champion: str = ""
    standings: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GameState:
    """The active game state."""

    game_year: int = 1976
    current_date: str = "19/03/1976"
    season_active: bool = False

    career: CareerState = field(default_factory=CareerState)
    championship: ChampionshipState = field(
        default_factory=ChampionshipState
    )

    # References to the historical world
    riders: Dict[str, Any] = field(default_factory=dict)
    clubs: Dict[str, Any] = field(default_factory=dict)
    fixtures: Dict[str, Any] = field(default_factory=dict)

    records: List[Any] = field(default_factory=list)
    historical_events: List[Any] = field(default_factory=list)


class GameStateManager:
    """
    Controls the active game state.

    The manager receives a SpeedwayWorld from WorldBuilder.
    It does not reload the historical JSON databases.
    """

    def __init__(self, world=None):

        self.world = None
        self.state = GameState()

        if world is not None:
            self.load_world(world)

    # ----------------------------------------------------------
    # WORLD
    # ----------------------------------------------------------

    def load_world(self, world):

        if world is None:
            raise ValueError("Cannot load an empty SpeedwayWorld")

        self.world = world

        self.state.game_year = world.season
        self.state.current_date = self._get_world_start_date(world)

        self.state.riders = world.riders
        self.state.clubs = world.clubs
        self.state.fixtures = world.fixtures

        self.state.season_active = False

        return self.state

    def _get_world_start_date(self, world):

        fixtures = world.fixtures

        if not fixtures:
            return "19/03/1976"

        first_fixture = next(iter(fixtures.values()))

        if hasattr(first_fixture, "meeting_date"):
            return first_fixture.meeting_date

        if hasattr(first_fixture, "date"):
            return first_fixture.date

        return "19/03/1976"

    # ----------------------------------------------------------
    # NEW GAME
    # ----------------------------------------------------------

    def create_new_game(
        self,
        manager_name: str,
        club_id: str,
    ):

        if self.world is None:
            raise RuntimeError(
                "A SpeedwayWorld must be loaded before starting a game"
            )

        if club_id not in self.state.clubs:
            raise ValueError(
                f"Unknown club ID: {club_id}"
            )

        self.state.career = CareerState(
            manager_name=manager_name,
            club_id=club_id,
        )

        self.state.season_active = True

        return self.state

    # ----------------------------------------------------------
    # DATE
    # ----------------------------------------------------------

    def update_date(self, new_date: str):

        self.state.current_date = new_date

    # ----------------------------------------------------------
    # CLUB
    # ----------------------------------------------------------

    def get_manager_club(self):

        club_id = self.state.career.club_id

        if club_id is None:
            return None

        return self.state.clubs.get(club_id)

    # ----------------------------------------------------------
    # RIDERS
    # ----------------------------------------------------------

    def get_rider(self, rider_id: str):

        return self.state.riders.get(rider_id)

    def get_club_riders(self, club_id: str):

        club = self.state.clubs.get(club_id)

        if club is None:
            return []

        club_name = getattr(
            club,
            "name",
            "",
        )

        return [
            rider
            for rider in self.state.riders.values()
            if getattr(rider, "club", "") == club_name
        ]

    # ----------------------------------------------------------
    # FIXTURES
    # ----------------------------------------------------------

    def get_fixture(self, fixture_id: str):

        return self.state.fixtures.get(fixture_id)

    def get_club_fixtures(self, club_id: str):

        club = self.state.clubs.get(club_id)

        if club is None:
            return []

        club_name = getattr(
            club,
            "name",
            "",
        )

        fixtures = []

        for fixture in self.state.fixtures.values():

            if (
                getattr(fixture, "home_team", "") == club_name
                or getattr(fixture, "away_team", "") == club_name
            ):
                fixtures.append(fixture)

        return fixtures

    # ----------------------------------------------------------
    # CHAMPIONSHIP
    # ----------------------------------------------------------

    def update_champion(self, name: str):

        self.state.championship.champion = name

    def update_standings(self, standings):

        self.state.championship.standings = standings

    # ----------------------------------------------------------
    # HISTORY
    # ----------------------------------------------------------

    def add_historical_event(self, event):

        self.state.historical_events.append(event)

    # ----------------------------------------------------------
    # RECORDS
    # ----------------------------------------------------------

    def add_record(self, record):

        self.state.records.append(record)

    # ----------------------------------------------------------
    # CAREER
    # ----------------------------------------------------------

    def progress_career_year(self):

        self.state.career.career_years += 1
        self.state.game_year += 1

    # ----------------------------------------------------------
    # EXPORT
    # ----------------------------------------------------------

    def export_state(self):

        return asdict(self.state)

    # ----------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------

    def summary(self):

        manager_club = self.get_manager_club()

        club_name = ""

        if manager_club is not None:
            club_name = getattr(
                manager_club,
                "name",
                "",
            )

        return {
            "year": self.state.game_year,
            "date": self.state.current_date,
            "season_active": self.state.season_active,
            "manager": self.state.career.manager_name,
            "club_id": self.state.career.club_id,
            "club": club_name,
            "riders": len(self.state.riders),
            "clubs": len(self.state.clubs),
            "fixtures": len(self.state.fixtures),
            "champion": self.state.championship.champion,
        }

    # ----------------------------------------------------------
    # VALIDATION
    # ----------------------------------------------------------

    def validate_state(self):

        if self.world is None:
            return False

        if self.state.game_year != self.world.season:
            return False

        if len(self.state.riders) != len(self.world.riders):
            return False

        if len(self.state.clubs) != len(self.world.clubs):
            return False

        if len(self.state.fixtures) != len(self.world.fixtures):
            return False

        return True


# Global manager instance
game_state = GameStateManager()


if __name__ == "__main__":

    from core.world_builder import WorldBuilder

    world = WorldBuilder().build()

    manager = GameStateManager(world)

    manager.create_new_game(
        "Shaun",
        "BEL001",
    )

    print("GAME STATE: PASS")
    print(manager.summary())