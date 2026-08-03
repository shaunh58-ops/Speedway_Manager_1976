"""
British League Speedway Manager

Application Controller

Version: Alpha 0.1

Controls application flow and communication
between UI and game engine.
"""


from __future__ import annotations


from typing import Optional



from core.logger import get_logger


from core.event_bus import event_bus


from core.world_builder import world_builder



log = get_logger(

    "ApplicationController"

)



# ==========================================================
# APPLICATION CONTROLLER
# ==========================================================


class ApplicationController:


    def __init__(self):


        self.main_window = None


        self.world = None


        self.current_club = None


        self.current_manager = None


        self.game_started = False



        log.info(

            "Application controller created"

        )



    # ======================================================
    # CONNECT MAIN WINDOW
    # ======================================================


    def attach_window(
        self,
        window,
    ):


        self.main_window = window



    # ======================================================
    # START NEW GAME
    # ======================================================


    def new_game(self):


        log.info(

            "Starting new game"

        )



        self.world = world_builder.build()



        self.game_started = True



        event_bus.publish(

            "new_game_started"

        )



        return self.world



    # ======================================================
    # CLUB SELECTION
    # ======================================================


    def select_club(
        self,
        club,
    ):


        self.current_club = club



        log.info(

            f"Selected club: {club.name}"

        )



        event_bus.publish(

            "club_selected",

            club=club

        )



    # ======================================================
    # GET CURRENT CLUB
    # ======================================================


    def get_current_club(self):


        return self.current_club



    # ======================================================
    # NAVIGATION
    # ======================================================


    def show_screen(
        self,
        screen,
    ):


        if self.main_window:


            self.main_window.show_screen(

                screen

            )



    # ======================================================
    # DASHBOARD DATA
    # ======================================================


    def get_dashboard_data(self):


        if not self.current_club:


            return {}



        return {


            "club":

            self.current_club.name,


            "venue":

            self.current_club.venue,


            "riders":

            len(

                self.current_club.riders

            )

        }



    # ======================================================
    # SAVE GAME PLACEHOLDER
    # ======================================================


    def save_game(self):


        log.info(

            "Save game requested"

        )


        # Save Game Manager
        # will connect here.



    # ======================================================
    # LOAD GAME PLACEHOLDER
    # ======================================================


    def load_game(self):


        log.info(

            "Load game requested"

        )


        # Load system
        # will connect here.



    # ======================================================
    # EXIT GAME
    # ======================================================


    def exit_game(self):


        log.info(

            "Closing application"

        )



        if self.main_window:


            self.main_window.close()


