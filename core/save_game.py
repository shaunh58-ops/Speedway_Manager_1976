"""
Speedway Game Engine

Save Game Module

Version: 1.0

Handles game persistence.

Features:

- Save careers
- Load careers
- JSON storage
- Backup saves
- Version tracking

"""


import json

import shutil

from pathlib import Path

from datetime import datetime



class SaveGame:



    SAVE_VERSION = "1.0"



    def __init__(
            self,
            save_folder="saves"
    ):


        self.save_folder = Path(
            save_folder
        )


        self.save_folder.mkdir(
            exist_ok=True
        )



    # =========================================================
    # SERIALISATION HELPERS
    # =========================================================


    def rider_to_dict(
            self,
            rider
    ):


        return {


            "id":
                rider.id,


            "name":
                rider.name,


            "nationality":
                rider.nationality,


            "age":
                rider.age,


            "historical_cma":
                rider.historical_cma,


            "current_cma":
                rider.current_cma,


            "potential":
                rider.potential,


            "experience":
                rider.experience,


            "injuries":
                rider.injuries,


            "retired":
                rider.retired,


            "club_id":
                rider.club_id,


            "career_years":
                rider.career_years,


            "form":
                rider.form

        }



    def club_to_dict(
            self,
            club
    ):


        return {


            "id":
                club.id,


            "name":
                club.name,


            "location":
                club.location,


            "founded":
                club.founded,


            "stadium":
                club.stadium,


            "league":
                club.league,


            "wins":
                club.wins,


            "defeats":
                club.defeats,


            "points":
                club.points,


            "rider_ids":

                [

                    rider.id

                    for rider in club.squad

                ]

        }



    # =========================================================
    # SAVE GAME
    # =========================================================


    def save(
            self,
            filename,
            season_manager,
            rider_manager,
            team_manager,
            championship_engine
    ):


        save_path = (

            self.save_folder /
            filename

        )



        data = {


            "save_version":

                self.SAVE_VERSION,


            "created":

                datetime.now()
                .isoformat(),


            "season":

                season_manager.year,


            "riders":

                [

                    self.rider_to_dict(rider)

                    for rider

                    in rider_manager.riders.values()

                ],


            "clubs":

                [

                    self.club_to_dict(club)

                    for club

                    in team_manager.clubs.values()

                ],


            "league_history":

                championship_engine.league_history,


            "rider_history":

                championship_engine.rider_history,


            "hall_of_fame":

                championship_engine.hall_of_fame

        }



        with open(

            save_path,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                data,

                file,

                indent=4

            )



        return save_path



    # =========================================================
    # LOAD GAME
    # =========================================================


    def load(
            self,
            filename
    ):


        save_path = (

            self.save_folder /
            filename

        )



        if not save_path.exists():

            return None



        with open(

            save_path,

            "r",

            encoding="utf-8"

        ) as file:


            data = json.load(
                file
            )



        return data



    # =========================================================
    # BACKUP SYSTEM
    # =========================================================


    def backup(
            self,
            filename
    ):


        source = (

            self.save_folder /
            filename

        )


        if not source.exists():

            return False



        backup_name = (

            filename.replace(

                ".json",

                ""

            )

            +

            "_backup.json"

        )



        shutil.copy(

            source,

            self.save_folder /
            backup_name

        )


        return True



    # =========================================================
    # SAVE MANAGEMENT
    # =========================================================


    def list_saves(self):


        return [

            file.name

            for file

            in self.save_folder.glob(
                "*.json"
            )

        ]



    def delete_save(
            self,
            filename
    ):


        path = (

            self.save_folder /
            filename

        )


        if path.exists():

            path.unlink()

            return True


        return False



# =============================================================
# TEST MODULE
# =============================================================


if __name__ == "__main__":


    saver = SaveGame()


    print(

        saver.list_saves()

    )
