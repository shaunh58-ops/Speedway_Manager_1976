"""
Speedway Game Engine

Game Configuration Module

Version: 1.0

Central configuration system
for all game modes and settings.

"""


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict
import json
import os



# ==========================================================
# DATA STRUCTURE
# ==========================================================


@dataclass(slots=True)
class GameConfig:


    game_version: str = "1.0"


    game_title: str = "Speedway Career Manager"


    start_year: int = 1976


    current_year: int = 1976


    game_mode: str = "Historical"


    difficulty: str = "Normal"


    ruleset: str = "British League"



    # Database paths

    rider_database: str = "data/riders.json"

    team_database: str = "data/teams.json"

    fixture_database: str = "data/fixtures.json"

    venue_database: str = "data/venues.json"



    # Simulation settings

    realistic_finances: bool = True

    injuries_enabled: bool = True

    retirements_enabled: bool = True

    weather_enabled: bool = True

    historical_equipment: bool = True



    # Career settings

    youth_development: bool = True

    rider_progression_speed: str = "Normal"


    # AI settings

    ai_strength: str = "Normal"



    custom_settings: Dict = field(

        default_factory=dict

    )



# ==========================================================
# CONFIG MANAGER
# ==========================================================


class GameConfigManager:


    def __init__(self):

        self.config = GameConfig()



    # ======================================================
    # UPDATE SETTINGS
    # ======================================================


    def update_setting(
            self,
            setting,
            value
    ):


        if hasattr(

            self.config,

            setting

        ):


            setattr(

                self.config,

                setting,

                value

            )


            return True



        return False



    # ======================================================
    # HISTORICAL PRESET
    # ======================================================


    def load_historical_mode(
            self,
            year
    ):


        self.config.start_year = year

        self.config.current_year = year

        self.config.game_mode = "Historical"


        self.config.historical_equipment = True

        self.config.ruleset = "British League"



    # ======================================================
    # MODERN PRESET
    ======================================================


    def load_modern_mode(
            self,
            year
    ):


        self.config.start_year = year

        self.config.current_year = year

        self.config.game_mode = "Modern"


        self.config.historical_equipment = False

        self.config.ruleset = "Modern Speedway"



    # ======================================================
    # CUSTOM MODE
    ======================================================


    def load_custom_mode(
            self,
            settings
    ):


        self.config.game_mode = "Custom"


        self.config.custom_settings = settings



    # ======================================================
    # SAVE CONFIG
    ======================================================


    def save_config(
            self,
            filepath="config/game_config.json"
    ):


        directory = os.path.dirname(

            filepath

        )


        if directory:

            os.makedirs(

                directory,

                exist_ok=True

            )


        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                asdict(

                    self.config

                ),

                file,

                indent=4

            )



    # ======================================================
    # LOAD CONFIG
    ======================================================


    def load_config(
            self,
            filepath="config/game_config.json"
    ):


        if not os.path.exists(filepath):

            return False



        with open(

            filepath,

            "r",

            encoding="utf-8"

        ) as file:


            data = json.load(

                file

            )


        self.config = GameConfig(

            **data

        )


        return True



    # ======================================================
    # REPORT
    ======================================================


    def report(self):


        return asdict(

            self.config

        )



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = GameConfigManager()


    manager.load_historical_mode(

        1976

    )


    print(

        manager.report()

    )
