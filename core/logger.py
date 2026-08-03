"""
Speedway Game Engine

Logger Module

Version: 1.0

Professional logging system
for game events and diagnostics.

"""


from __future__ import annotations

import logging
import os

from datetime import datetime
from typing import Optional



# ==========================================================
# LOGGER MANAGER
# ==========================================================


class GameLogger:


    def __init__(
            self,
            name="SpeedwayEngine",
            log_directory="logs",
            level=logging.INFO
    ):


        self.name = name

        self.log_directory = log_directory


        os.makedirs(

            log_directory,

            exist_ok=True

        )


        filename = (

            datetime.now()

            .strftime(

                "%Y-%m-%d"

            )

            +

            "_speedway.log"

        )


        self.log_file = os.path.join(

            log_directory,

            filename

        )


        self.logger = logging.getLogger(

            name

        )


        self.logger.setLevel(

            level

        )


        if not self.logger.handlers:


            self._configure()



    # ======================================================
    # CONFIGURE LOGGER
    # ======================================================


    def _configure(self):


        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )


        file_handler = logging.FileHandler(

            self.log_file,

            encoding="utf-8"

        )


        file_handler.setFormatter(

            formatter

        )


        console_handler = logging.StreamHandler()


        console_handler.setFormatter(

            formatter

        )


        self.logger.addHandler(

            file_handler

        )


        self.logger.addHandler(

            console_handler

        )



    # ======================================================
    # BASIC LOGGING
    ======================================================


    def debug(
            self,
            message
    ):


        self.logger.debug(

            message

        )



    def info(
            self,
            message
    ):


        self.logger.info(

            message

        )



    def warning(
            self,
            message
    ):


        self.logger.warning(

            message

        )



    def error(
            self,
            message
    ):


        self.logger.error(

            message

        )



    def critical(
            self,
            message
    ):


        self.logger.critical(

            message

        )



    # ======================================================
    # GAME EVENTS
    ======================================================


    def race_event(
            self,
            event
    ):


        self.info(

            f"RACE EVENT: {event}"

        )



    def transfer_event(
            self,
            event
    ):


        self.info(

            f"TRANSFER: {event}"

        )



    def injury_event(
            self,
            event
    ):


        self.warning(

            f"INJURY: {event}"

        )



    def financial_event(
            self,
            event
    ):


        self.info(

            f"FINANCE: {event}"

        )



    # ======================================================
    # DATABASE EVENTS
    ======================================================


    def database_error(
            self,
            database,
            issue
    ):


        self.error(

            f"DATABASE ERROR | {database}: {issue}"

        )



    def database_warning(
            self,
            database,
            issue
    ):


        self.warning(

            f"DATABASE WARNING | {database}: {issue}"

        )



    # ======================================================
    # SAVE GAME EVENTS
    ======================================================


    def save_event(
            self,
            filename
    ):


        self.info(

            f"GAME SAVED: {filename}"

        )



    def load_event(
            self,
            filename
    ):


        self.info(

            f"GAME LOADED: {filename}"

        )



    # ======================================================
    # EXCEPTION LOGGER
    ======================================================


    def exception(
            self,
            message,
            error: Optional[Exception] = None
    ):


        if error:


            self.logger.exception(

                f"{message}: {error}"

            )


        else:


            self.logger.exception(

                message

            )



# ==========================================================
# GLOBAL LOGGER INSTANCE
# ==========================================================


game_logger = GameLogger()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    logger = GameLogger()


    logger.info(

        "Speedway Engine Started"

    )


    logger.race_event(

        "1976 British League Opening Fixture"

    )


    logger.warning(

        "Weather conditions deteriorating"

    )
