"""
British League Speedway Manager

Game Loop

Version: 0.3.2

Controls the progression of the 1976 season.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, List

from core.logger import get_logger
from core.game_state_manager import GameStateManager


log = get_logger("GameLoop")


@dataclass
class LoopSettings:

    paused: bool = False
    auto_run: bool = False


class GameLoop:
    """
    Advances the historical Speedway season.
    """

    def __init__(
        self,
        game_state: GameStateManager,
    ):

        self.game_state = game_state

        self.settings = LoopSettings()

        self.running = False

        self.tasks: List[Callable] = []

        self.processed_fixtures = []


    # --------------------------------------------------
    # TASKS
    # --------------------------------------------------

    def register_task(self, task):

        self.tasks.append(task)


    # --------------------------------------------------
    # CONTROL
    # --------------------------------------------------

    def start(self):

        self.running = True

        log.info(
            "Game loop started"
        )


    def stop(self):

        self.running = False

        log.info(
            "Game loop stopped"
        )


    # --------------------------------------------------
    # DAILY TICK
    # --------------------------------------------------

    def tick(self):

        if not self.running:
            return

        if self.settings.paused:
            return


        self.process_daily_fixtures()

        self.process_tasks()

        self.advance_date()


    # --------------------------------------------------
    # FIXTURES
    # --------------------------------------------------

    def process_daily_fixtures(self):

        current_date = (
            self.game_state.state.current_date
        )


        todays_fixtures = [

            fixture

            for fixture

            in self.game_state.state.fixtures.values()

            if fixture.meeting_date == current_date

        ]


        for fixture in todays_fixtures:

            log.info(
                "TODAY: %s vs %s",
                fixture.home_team,
                fixture.away_team,
            )


            self.processed_fixtures.append(
                fixture.fixture_id
            )


    # --------------------------------------------------
    # TASK PROCESSING
    # --------------------------------------------------

    def process_tasks(self):

        for task in self.tasks:

            try:

                task()

            except Exception:

                log.exception(
                    "Game task failed"
                )


    # --------------------------------------------------
    # DATE ADVANCEMENT
    # --------------------------------------------------

    def advance_date(self):

        current = datetime.strptime(
            self.game_state.state.current_date,
            "%d/%m/%Y",
        )


        current += timedelta(days=1)


        self.game_state.update_date(
            current.strftime("%d/%m/%Y")
        )


    # --------------------------------------------------
    # RUN DAYS
    # --------------------------------------------------

    def run_days(
        self,
        days: int,
    ):

        self.start()


        for _ in range(days):

            self.tick()


        self.stop()


    # --------------------------------------------------
    # STATUS
    # --------------------------------------------------

    def status(self):

        return {

            "running":
                self.running,

            "date":
                self.game_state.state.current_date,

            "fixtures_processed":
                len(self.processed_fixtures),

            "tasks":
                len(self.tasks),
        }


if __name__ == "__main__":

    from core.world_builder import WorldBuilder


    world = WorldBuilder().build()


    state = GameStateManager(world)


    state.create_new_game(
        "Player",
        "BEL001",
    )


    loop = GameLoop(state)


    loop.run_days(10)


    print(loop.status())