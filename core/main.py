"""
Speedway Game Engine

Main Application Controller

Version: 1.0

Starts and controls the Speedway simulation.

"""



from database_loader import DatabaseLoader

from rider_manager import RiderManager

from team_manager import TeamManager

from race_engine import RaceEngine

from season_manager import SeasonManager

from championship_engine import ChampionshipEngine

from save_game import SaveGame



class SpeedwayGame:



    def __init__(self):


        print(
            "================================"
        )

        print(
            " Speedway Game Engine"
        )

        print(
            " Historical Speedway Simulator"
        )

        print(
            "================================"
        )



        self.database = DatabaseLoader()


        self.rider_manager = RiderManager()


        self.team_manager = TeamManager()


        self.race_engine = RaceEngine()


        self.championship = ChampionshipEngine()


        self.save_system = SaveGame()



        self.season = None



    # =========================================================
    # INITIALISE GAME
    # =========================================================


    def initialise(self):


        print(
            "\nLoading databases..."
        )



        self.database.load_all()



        self.rider_manager.load_riders(

            self.database.riders

        )



        self.team_manager.load_clubs(

            self.database.clubs

        )



        print(

            "Game database ready."

        )



    # =========================================================
    # CREATE SEASON
    # =========================================================


    def create_season(
            self,
            year
    ):


        self.season = SeasonManager(

            year,

            self.race_engine,

            self.team_manager,

            self.rider_manager

        )



        print(

            f"Season {year} created."

        )



    # =========================================================
    # SIMULATE SEASON
    # =========================================================


    def run_season(
            self
    ):


        if not self.season:


            print(
                "No active season."
            )

            return



        print(

            "Season simulation started..."

        )



        # Venue system will be connected here

        venues = {}



        results = self.season.run_full_season(

            venues

        )



        print(

            f"{len(results)} meetings completed."

        )



        summary = self.season.complete_season()



        print(

            summary

        )



    # =========================================================
    # SAVE GAME
    # =========================================================


    def save_game(
            self,
            filename="career_save.json"
    ):


        if not self.season:


            print(
                "Nothing to save."
            )

            return



        self.save_system.save(

            filename,

            self.season,

            self.rider_manager,

            self.team_manager,

            self.championship

        )



        print(

            "Game saved."

        )



    # =========================================================
    # STATUS REPORT
    # =========================================================


    def status_report(self):


        print(
            "\nGAME STATUS"
        )


        print(
            "------------"
        )


        print(

            self.rider_manager.database_summary()

        )


        print(

            f"Clubs: {len(self.team_manager.clubs)}"

        )



    # =========================================================
    # SIMPLE MENU
    # =========================================================


    def menu(self):


        while True:


            print(
                """

Speedway Game Menu

1. Database Status
2. Start 1976 Season
3. Run Season
4. Save Game
5. Exit

"""
            )


            choice = input(
                "Select option: "
            )



            if choice == "1":


                self.status_report()



            elif choice == "2":


                self.create_season(
                    1976
                )



            elif choice == "3":


                self.run_season()



            elif choice == "4":


                self.save_game()



            elif choice == "5":


                print(
                    "Goodbye."
                )

                break



            else:

                print(
                    "Invalid choice."
                )



# =============================================================
# APPLICATION START
# =============================================================


def main():


    game = SpeedwayGame()


    game.initialise()


    game.menu()



if __name__ == "__main__":


    main()
