"""
Speedway Game Engine

Event Bus Module

Version: 1.0

Central communication system
between all game modules.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any
from datetime import datetime



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class GameEvent:


    event_type: str

    data: Dict[str, Any]

    timestamp: datetime = field(

        default_factory=datetime.now

    )



# ==========================================================
# EVENT BUS
# ==========================================================


class EventBus:


    def __init__(self):

        self.listeners: Dict[
            str,
            List[Callable]
        ] = {}


        self.history: List[GameEvent] = []



    # ======================================================
    # SUBSCRIBE
    # ======================================================


    def subscribe(
            self,
            event_type,
            callback
    ):


        if event_type not in self.listeners:


            self.listeners[event_type] = []



        self.listeners[event_type].append(

            callback

        )



    # ======================================================
    # REMOVE SUBSCRIBER
    # ======================================================


    def unsubscribe(
            self,
            event_type,
            callback
    ):


        if event_type in self.listeners:


            if callback in self.listeners[event_type]:


                self.listeners[event_type].remove(

                    callback

                )



    # ======================================================
    # PUBLISH EVENT
    # ======================================================


    def publish(
            self,
            event_type,
            data=None
    ):


        if data is None:

            data = {}



        event = GameEvent(

            event_type,

            data

        )


        self.history.append(

            event

        )


        listeners = self.listeners.get(

            event_type,

            []

        )


        for callback in listeners:


            callback(

                event

            )


        return event



    # ======================================================
    # EVENT HISTORY
    # ======================================================


    def get_history(
            self,
            event_type=None
    ):


        if event_type:


            return [

                event

                for event

                in self.history

                if event.event_type == event_type

            ]



        return self.history



    # ======================================================
    # CLEAR HISTORY
    # ======================================================


    def clear_history(self):


        self.history.clear()



# ==========================================================
# GAME EVENT CONSTANTS
# ==========================================================


class Events:


    RACE_COMPLETED = "race_completed"

    HEAT_FINISHED = "heat_finished"

    RIDER_INJURED = "rider_injured"

    RIDER_TRANSFERRED = "rider_transferred"

    CONTRACT_SIGNED = "contract_signed"

    CHAMPIONSHIP_WON = "championship_won"

    RIDER_RETIRED = "rider_retired"

    WEATHER_CHANGED = "weather_changed"

    FINANCIAL_UPDATE = "financial_update"

    DATABASE_IMPORTED = "database_imported"

    SAVE_CREATED = "save_created"

    GAME_LOADED = "game_loaded"



# ==========================================================
# GLOBAL EVENT BUS
# ==========================================================


event_bus = EventBus()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    def race_listener(event):

        print(

            "Race Finished:",

            event.data

        )



    event_bus.subscribe(

        Events.RACE_COMPLETED,

        race_listener

    )



    event_bus.publish(

        Events.RACE_COMPLETED,

        {

            "winner":

            "Peter Collins",

            "score":

            "5-1"

        }

    )
