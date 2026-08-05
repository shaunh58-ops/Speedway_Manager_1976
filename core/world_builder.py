"""
British League Speedway Manager

World Builder

Version: 0.3.2

Builds the complete historical 1976 Speedway world from the
validated Rider, Club and Fixture databases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from core.logger import get_logger

from core.databases.rider_database_manager import (
    Rider,
    RiderDatabaseManager,
)

from core.databases.club_database_manager import (
    Club,
    ClubDatabaseManager,
)

from core.databases.fixture_database_manager import (
    Fixture,
    FixtureDatabaseManager,
)


log = get_logger("WorldBuilder")


# ----------------------------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "database"


DEFAULT_RIDER_DATABASE = (
    DATABASE_DIR / "riders_1976.json"
)

DEFAULT_CLUB_DATABASE = (
    DATABASE_DIR / "clubs_1976.json"
)

DEFAULT_FIXTURE_DATABASE = (
    DATABASE_DIR / "fixtures_1976.json"
)


# ----------------------------------------------------------------------
# GAME WORLD
# ----------------------------------------------------------------------


@dataclass
class SpeedwayWorld:
    """Complete historical 1976 Speedway game world."""

    riders: Dict[str, Rider] = field(
        default_factory=dict
    )

    clubs: Dict[str, Club] = field(
        default_factory=dict
    )

    fixtures: Dict[str, Fixture] = field(
        default_factory=dict
    )

    # Riders grouped by their historical club name.
    club_riders: Dict[str, List[Rider]] = field(
        default_factory=dict
    )

    season: int = 1976

    current_date: str = "01/01/1976"

    # World status
    built: bool = False


# ----------------------------------------------------------------------
# WORLD BUILDER
# ----------------------------------------------------------------------


class WorldBuilder:
    """Build the historical 1976 Speedway world."""

    def __init__(
        self,
        rider_database_path=None,
        club_database_path=None,
        fixture_database_path=None,
    ):

        self.rider_database_path = Path(
            rider_database_path
        ) if rider_database_path else DEFAULT_RIDER_DATABASE

        self.club_database_path = Path(
            club_database_path
        ) if club_database_path else DEFAULT_CLUB_DATABASE

        self.fixture_database_path = Path(
            fixture_database_path
        ) if fixture_database_path else DEFAULT_FIXTURE_DATABASE

        self.world: Optional[SpeedwayWorld] = None

    # ------------------------------------------------------------------
    # BUILD WORLD
    # ------------------------------------------------------------------

    def build(
        self,
        rider_file=None,
        club_file=None,
        fixture_file=None,
    ) -> SpeedwayWorld:
        """
        Load all historical databases and construct the 1976 world.
        """

        log.info(
            "Starting V0.3.2 world build"
        )

        rider_path = Path(
            rider_file
            or self.rider_database_path
        )

        club_path = Path(
            club_file
            or self.club_database_path
        )

        fixture_path = Path(
            fixture_file
            or self.fixture_database_path
        )

        self._check_database_file(
            rider_path,
            "Rider"
        )

        self._check_database_file(
            club_path,
            "Club"
        )

        self._check_database_file(
            fixture_path,
            "Fixture"
        )

        # --------------------------------------------------------------
        # Database managers
        # --------------------------------------------------------------

        rider_manager = RiderDatabaseManager(
            rider_path
        )

        club_manager = ClubDatabaseManager(
            club_path
        )

        fixture_manager = FixtureDatabaseManager(
            fixture_path
        )

        # --------------------------------------------------------------
        # Load historical data
        # --------------------------------------------------------------

        riders = rider_manager.load_database()

        clubs = club_manager.load_database()

        fixtures = fixture_manager.load_database()

        log.info(
            "Historical databases loaded: "
            "%s riders | %s clubs | %s fixtures",
            len(riders),
            len(clubs),
            len(fixtures),
        )

        # --------------------------------------------------------------
        # Build world
        # --------------------------------------------------------------

        world = SpeedwayWorld(
            riders=riders,
            clubs=clubs,
            fixtures=fixtures,
            season=1976,
            current_date=self._get_start_date(
                fixtures
            ),
        )

        # --------------------------------------------------------------
        # Build rider → club relationships
        # --------------------------------------------------------------

        self.assign_riders_to_clubs(
            world
        )

        # --------------------------------------------------------------
        # Validate fixture → club relationships
        # --------------------------------------------------------------

        self.validate_fixture_club_links(
            world
        )

        # --------------------------------------------------------------
        # Validate world
        # --------------------------------------------------------------

        world.built = True

        self.world = world

        self.validate_world()

        log.info(
            "V0.3.2 Speedway World created successfully"
        )

        return world

    # ------------------------------------------------------------------
    # FILE VALIDATION
    # ------------------------------------------------------------------

    @staticmethod
    def _check_database_file(
        path: Path,
        database_name: str,
    ) -> None:
        """Confirm a required historical database exists."""

        if not path.exists():
            raise FileNotFoundError(
                f"{database_name} database not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"{database_name} database path is not a file: {path}"
            )

    # ------------------------------------------------------------------
    # START DATE
    # ------------------------------------------------------------------

    @staticmethod
    def _get_start_date(
        fixtures: Dict[str, Fixture]
    ) -> str:
        """Return the earliest fixture date."""

        if not fixtures:
            return "01/01/1976"

        dates = [
            fixture.meeting_date
            for fixture in fixtures.values()
            if fixture.meeting_date
        ]

        if not dates:
            return "01/01/1976"

        return min(
            dates,
            key=lambda value: (
                int(value[6:10]),
                int(value[3:5]),
                int(value[0:2]),
            ),
        )

    # ------------------------------------------------------------------
    # RIDER → CLUB LINKS
    # ------------------------------------------------------------------

    @staticmethod
    def assign_riders_to_clubs(
        world: SpeedwayWorld
    ) -> None:
        """
        Build a clean mapping of club name → riders.

        Rider.club contains the historical team name.
        Club.name contains the historical club name.
        """

        world.club_riders.clear()

        for club in world.clubs.values():

            world.club_riders[
                club.name
            ] = []

        club_names = {
            club.name.casefold(): club.name
            for club in world.clubs.values()
        }

        for rider in world.riders.values():

            rider_club = (
                rider.club.strip().casefold()
            )

            canonical_name = club_names.get(
                rider_club
            )

            if canonical_name is None:

                raise ValueError(
                    "Rider references unknown club: "
                    f"{rider.name} -> {rider.club}"
                )

            world.club_riders[
                canonical_name
            ].append(rider)

        for club_name, riders in (
            world.club_riders.items()
        ):

            log.info(
                "%s: %s riders",
                club_name,
                len(riders),
            )

    # ------------------------------------------------------------------
    # FIXTURE → CLUB VALIDATION
    # ------------------------------------------------------------------

    @staticmethod
    def validate_fixture_club_links(
        world: SpeedwayWorld
    ) -> None:
        """Ensure every fixture references a known club."""

        known_clubs = {
            club.name.casefold()
            for club in world.clubs.values()
        }

        for fixture in world.fixtures.values():

            home = (
                fixture.home_team
                .strip()
                .casefold()
            )

            away = (
                fixture.away_team
                .strip()
                .casefold()
            )

            if home not in known_clubs:

                raise ValueError(
                    "Fixture references unknown home club: "
                    f"{fixture.home_team}"
                )

            if away not in known_clubs:

                raise ValueError(
                    "Fixture references unknown away club: "
                    f"{fixture.away_team}"
                )

    # ------------------------------------------------------------------
    # WORLD VALIDATION
    # ------------------------------------------------------------------

    def validate_world(
        self
    ) -> bool:
        """Validate the constructed Speedway world."""

        if self.world is None:
            raise RuntimeError(
                "No Speedway World has been built"
            )

        world = self.world

        if world.season != 1976:
            raise ValueError(
                f"Unexpected season: {world.season}"
            )

        if len(world.riders) != 152:
            raise ValueError(
                "Unexpected rider count: "
                f"{len(world.riders)}"
            )

        if len(world.clubs) != 19:
            raise ValueError(
                "Unexpected club count: "
                f"{len(world.clubs)}"
            )

        if len(world.fixtures) != 342:
            raise ValueError(
                "Unexpected fixture count: "
                f"{len(world.fixtures)}"
            )

        if len(world.club_riders) != 19:
            raise ValueError(
                "Club rider mapping is incomplete"
            )

        rider_count = sum(
            len(riders)
            for riders in world.club_riders.values()
        )

        if rider_count != len(world.riders):
            raise ValueError(
                "Club rider mapping does not contain "
                "all riders"
            )

        log.info(
            "World validation passed: "
            "1976 | %s riders | %s clubs | %s fixtures",
            len(world.riders),
            len(world.clubs),
            len(world.fixtures),
        )

        return True

    # ------------------------------------------------------------------
    # WORLD ACCESS
    # ------------------------------------------------------------------

    def get_world(
        self
    ) -> Optional[SpeedwayWorld]:
        """Return the currently built world."""

        return self.world


# ----------------------------------------------------------------------
# GLOBAL WORLD BUILDER
# ----------------------------------------------------------------------

world_builder = WorldBuilder()