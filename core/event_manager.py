"""
Speedway Game Engine

Event Manager Module

Version: 1.0

Coordinates all game systems through a central event bus.

"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Dict, List
import logging


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class GameEvent:
    """Represents a dispatched game event."""

    name: str
    payload: Dict[str, Any]


class EventManager:
    """
    Central event dispatcher.

    Other managers subscribe to named events.
    """

    def __init__(self):

        self._listeners: DefaultDict[
            str,
            List[Callable[[GameEvent], None]]
        ] = defaultdict(list)

        self.event_log: List[GameEvent] = []

    # =====================================================
    # SUBSCRIPTIONS
    # =====================================================

    def subscribe(
        self,
        event_name: str,
        callback: Callable[[GameEvent], None]
    ) -> None:

        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)

    def unsubscribe(
        self,
        event_name: str,
        callback: Callable[[GameEvent], None]
    ) -> None:

        if callback in self._listeners[event_name]:
            self._listeners[event_name].remove(callback)

    # =====================================================
    # DISPATCH
    # =====================================================

    def dispatch(
        self,
        event_name: str,
        **payload: Any
    ) -> GameEvent:

        event = GameEvent(
            name=event_name,
            payload=payload
        )

        self.event_log.append(event)

        logger.debug(
            "Dispatching event %s",
            event_name
        )

        for listener in list(self._listeners[event_name]):

            try:
                listener(event)

            except Exception:

                logger.exception(
                    "Event handler failed for '%s'",
                    event_name
                )

        return event

    # =====================================================
    # STANDARD EVENTS
    # =====================================================

    def season_started(
        self,
        season: int
    ):

        return self.dispatch(
            "season_started",
            season=season
        )

    def season_finished(
        self,
        season: int
    ):

        return self.dispatch(
            "season_finished",
            season=season
        )

    def week_started(
        self,
        week: int
    ):

        return self.dispatch(
            "week_started",
            week=week
        )

    def week_finished(
        self,
        week: int
    ):

        return self.dispatch(
            "week_finished",
            week=week
        )

    def meeting_started(
        self,
        fixture
    ):

        return self.dispatch(
            "meeting_started",
            fixture=fixture
        )

    def meeting_finished(
        self,
        result
    ):

        return self.dispatch(
            "meeting_finished",
            result=result
        )

    def transfer_window_opened(
        self,
        season: int
    ):

        return self.dispatch(
            "transfer_window_opened",
            season=season
        )

    def transfer_window_closed(
        self,
        season: int
    ):

        return self.dispatch(
            "transfer_window_closed",
            season=season
        )

    def youth_intake(
        self,
        season: int
    ):

        return self.dispatch(
            "youth_intake",
            season=season
        )

    def rider_retired(
        self,
        rider
    ):

        return self.dispatch(
            "rider_retired",
            rider=rider
        )

    def rider_injured(
        self,
        rider,
        severity: str
    ):

        return self.dispatch(
            "rider_injured",
            rider=rider,
            severity=severity
        )

    def championship_finished(
        self,
        standings
    ):

        return self.dispatch(
            "championship_finished",
            standings=standings
        )

    # =====================================================
    # LOGGING
    # =====================================================

    def recent_events(
        self,
        limit: int = 20
    ) -> List[GameEvent]:

        return self.event_log[-limit:]

    def clear_log(self):

        self.event_log.clear()

    def summary(self):

        counts = {}

        for event in self.event_log:

            counts[event.name] = (
                counts.get(event.name, 0) + 1
            )

        return counts


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    manager = EventManager()

    def on_season(event):

        print(
            f"Season {event.payload['season']} started."
        )

    manager.subscribe(
        "season_started",
        on_season
    )

    manager.season_started(1976)

    print(
        manager.summary()
    )
