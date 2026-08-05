"""
Speedway Game Engine

Logger Module

Version: 0.3.1

Professional logging system for
game events and diagnostics.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional


class GameLogger:
    """Central logging system for the Speedway Manager engine."""

    def __init__(
        self,
        name: str = "SpeedwayEngine",
        log_directory: str = "logs",
        level: int = logging.INFO,
    ):
        self.name = name
        self.log_directory = log_directory

        os.makedirs(
            self.log_directory,
            exist_ok=True,
        )

        filename = (
            datetime.now().strftime("%Y-%m-%d")
            + "_speedway.log"
        )

        self.log_file = os.path.join(
            self.log_directory,
            filename,
        )

        self.logger = logging.getLogger(
            self.name
        )

        self.logger.setLevel(level)

        if not self.logger.handlers:
            self._configure()

    def _configure(self):
        """Configure file and console logging."""

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            self.log_file,
            encoding="utf-8",
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

    # --------------------------------------------------
    # BASIC LOGGING
    # --------------------------------------------------

    def debug(
        self,
        message,
    ):
        self.logger.debug(message)

    def info(
        self,
        message,
        *args,
    ):
        self.logger.info(
            message,
            *args,
        )

    def warning(
        self,
        message,
        *args,
    ):
        self.logger.warning(
            message,
            *args,
        )

    def error(
        self,
        message,
        *args,
    ):
        self.logger.error(
            message,
            *args,
        )

    def critical(
        self,
        message,
        *args,
    ):
        self.logger.critical(
            message,
            *args,
        )

    # --------------------------------------------------
    # GAME EVENTS
    # --------------------------------------------------

    def race_event(
        self,
        event,
    ):
        self.info(
            "RACE EVENT: %s",
            event,
        )

    def transfer_event(
        self,
        event,
    ):
        self.info(
            "TRANSFER: %s",
            event,
        )

    def injury_event(
        self,
        event,
    ):
        self.warning(
            "INJURY: %s",
            event,
        )

    def financial_event(
        self,
        event,
    ):
        self.info(
            "FINANCE: %s",
            event,
        )

    # --------------------------------------------------
    # DATABASE EVENTS
    # --------------------------------------------------

    def database_error(
        self,
        database,
        issue,
    ):
        self.error(
            "DATABASE ERROR | %s: %s",
            database,
            issue,
        )

    def database_warning(
        self,
        database,
        issue,
    ):
        self.warning(
            "DATABASE WARNING | %s: %s",
            database,
            issue,
        )

    # --------------------------------------------------
    # SAVE GAME EVENTS
    # --------------------------------------------------

    def save_event(
        self,
        filename,
    ):
        self.info(
            "GAME SAVED: %s",
            filename,
        )

    def load_event(
        self,
        filename,
    ):
        self.info(
            "GAME LOADED: %s",
            filename,
        )

    # --------------------------------------------------
    # EXCEPTION LOGGER
    # --------------------------------------------------

    def exception(
        self,
        message,
        error: Optional[Exception] = None,
    ):
        if error is not None:
            self.logger.exception(
                "%s: %s",
                message,
                error,
            )
        else:
            self.logger.exception(
                message
            )


# --------------------------------------------------
# GLOBAL LOGGER INSTANCE
# --------------------------------------------------

game_logger = GameLogger()


# --------------------------------------------------
# COMPATIBILITY FUNCTION
# --------------------------------------------------

def get_logger(
    name: str = "SpeedwayEngine",
):
    """
    Return a standard Python logger.

    Database managers use this function so that
    existing engine code remains compatible.
    """

    return logging.getLogger(name)


# --------------------------------------------------
# TEST MODULE
# --------------------------------------------------

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