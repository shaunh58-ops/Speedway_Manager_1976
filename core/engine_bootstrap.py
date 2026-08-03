"""
Speedway Game Engine

Engine Bootstrap Module

Version: 1.0

Controls the complete startup
and shutdown process of the engine.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


from game_config import GameConfigManager
from dependency_manager import DependencyManager
from logger import GameLogger
from event_bus import EventBus



# ==========================================================
# ENGINE STATUS
# ==========================================================


@dataclass(slots=True)
class EngineStatus:


    running: bool = False

    systems_loaded: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )



# ==========================================================
# ENGINE BOOTSTRAP
# ==========================================================


class EngineBootstrap:


    def __init__(self):


        self.config_manager = GameConfigManager()


        self.logger = GameLogger()


        self.event_bus = EventBus()


        self.dependencies = DependencyManager()


        self.status = EngineStatus()



    # ======================================================
    # REGISTER CORE SYSTEMS
    # ======================================================


    def register_systems(self):


        self.dependencies.register_module(

            "configuration",

            "1.0",

            self.load_configuration

        )


        self.dependencies.register_module(

            "logging",

            "1.0",

            self.load_logging,

            [

                "configuration"

            ]

        )


        self.dependencies.register_module(

            "events",

            "1.0",

            self.load_events,

            [

                "logging"

            ]

        )


        self.dependencies.register_module(

            "database",

            "1.0",

            self.load_database,

            [

                "configuration",

                "logging"

            ]

        )



    # ======================================================
    # LOAD CONFIGURATION
    # ======================================================


    def load_configuration(self):


        self.status.systems_loaded.append(

            "Configuration"

        )


        self.logger.info(

            "Configuration system loaded"

        )



    # ======================================================
    # LOAD LOGGER
    # ======================================================


    def load_logging(self):


        self.status.systems_loaded.append(

            "Logging"

        )


        self.logger.info(

            "Logging system loaded"

        )



    # ======================================================
    # LOAD EVENTS
    # ======================================================


    def load_events(self):


        self.status.systems_loaded.append(

            "Event Bus"

        )


        self.logger.info(

            "Event system loaded"

        )



    # ======================================================
    # LOAD DATABASE
    # ======================================================


    def load_database(self):


        self.status.systems_loaded.append(

            "Database"

        )


        self.logger.info(

            "Database system loaded"

        )



    # ======================================================
    # START ENGINE
    ======================================================


    def start(self):


        try:


            self.logger.info(

                "Starting Speedway Game Engine"

            )


            self.register_systems()


            self.dependencies.load_all()



            self.status.running = True



            self.logger.info(

                "Engine successfully started"

            )


            return True



        except Exception as error:


            self.status.errors.append(

                str(error)

            )


            self.logger.exception(

                "Engine startup failed",

                error

            )


            return False



    # ======================================================
    # SHUTDOWN
    ======================================================


    def shutdown(self):


        self.logger.info(

            "Shutting down Speedway Engine"

        )


        self.status.running = False



    # ======================================================
    # HEALTH REPORT
    ======================================================


    def health_report(self):


        return {


            "running":

                self.status.running,


            "systems":

                self.status.systems_loaded,


            "errors":

                self.status.errors,


            "dependencies":

                self.dependencies.health_check()

        }



# ==========================================================
# GLOBAL ENGINE INSTANCE
# ==========================================================


engine = EngineBootstrap()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    engine.start()


    print(

        engine.health_report()

    )


    engine.shutdown()
