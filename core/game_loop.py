"""
Speedway Game Engine

Game Loop Module

Version: 1.0

Controls the continuous simulation
of the Speedway world.

"""


from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, List


from game_state_manager import GameStateManager
from event_bus import EventBus, Events
from logger import GameLogger



# ==========================================================
# DATA STRUCTURE
# ==========================================================


@dataclass(slots=True)
class LoopSettings:


    simulation_speed: str = "Normal"


    paused: bool = False


    auto_run: bool = False



# ==========================================================
# GAME LOOP
# ==========================================================


class GameLoop:


    def __init__(
            self,
            game_state: GameStateManager,
            event_bus: EventBus,
            logger: GameLogger
    ):


        self.game_state = game_state

        self.event_bus = event_bus

        self.logger = logger


        self.settings = LoopSettings()


        self.running = False


        self.tasks: List[Callable] = []



    # ======================================================
    # REGISTER TASK
    # ======================================================


    def register_task(
            self,
            task
    ):


        self.tasks.append(

            task

        )



    # ======================================================
    # START LOOP
    # ======================================================


    def start(self):


        self.running = True


        self.logger.info(

            "Game loop started"

        )



    # ======================================================
    # STOP LOOP
    # ======================================================


    def stop(self):


        self.running = False


        self.logger.info(

            "Game loop stopped"

        )



    # ======================================================
    # DAILY TICK
    # ======================================================


    def tick(self):


        if not self.running:

            return



        if self.settings.paused:

            return



        self.logger.debug(

            "Processing daily simulation tick"

        )



        self.process_tasks()


        self.advance_time()



    # ======================================================
    # PROCESS SYSTEM TASKS
    ======================================================


    def process_tasks(self):


        for task in self.tasks:


            try:


                task()



            except Exception as error:


                self.logger.exception(

                    "Game task failed",

                    error

                )



    # ======================================================
    # ADVANCE DATE
    ======================================================


    def advance_time(self):


        current = datetime.strptime(

            self.game_state.state.current_date,

            "%Y-%m-%d"

        )


        current += timedelta(days=1)


        self.game_state.update_date(

            current.strftime(

                "%Y-%m-%d"

            )

        )


        self.event_bus.publish(

            Events.GAME_LOADED,

            {

                "date":

                current.strftime(

                    "%Y-%m-%d"

                )

            }

        )



    # ======================================================
    # RUN DAYS
    ======================================================


    def run_days(
            self,
            days
    ):


        self.start()



        for _ in range(days):


            self.tick()



        self.stop()



    # ======================================================
    # STATUS
    ======================================================


    def status(self):


        return {


            "running":

            self.running,


            "date":

            self.game_state.state.current_date,


            "tasks":

            len(self.tasks)

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    from game_state_manager import game_state

    from event_bus import event_bus

    from logger import game_logger



    game_state.create_new_game(

        1976,

        "Player",

        1

    )


    loop = GameLoop(

        game_state,

        event_bus,

        game_logger

    )


    loop.run_days(

        5

    )


    print(

        loop.status()

    )
