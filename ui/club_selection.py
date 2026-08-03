"""
British League Speedway Manager

Club Selection Screen

Version: Alpha 0.1

Allows the player to choose their Speedway club.
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox
)


from PySide6.QtCore import Qt


from core.logger import get_logger



log = get_logger(
    "ClubSelection"
)



# ==========================================================
# CLUB SELECTION SCREEN
# ==========================================================


class ClubSelection(QWidget):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.clubs = []


        self.setup_ui()



    # ======================================================
    # BUILD UI
    ======================================================


    def setup_ui(self):


        layout = QVBoxLayout()



        self.setLayout(

            layout

        )



        # Title


        title = QLabel(

            "🏁 Choose Your Speedway Club\n"
            "British League 1976"

        )


        title.setAlignment(

            Qt.AlignCenter

        )


        title.setObjectName(

            "screen_title"

        )


        layout.addWidget(

            title

        )



        # Club List


        self.club_list = QListWidget()



        layout.addWidget(

            self.club_list

        )



        # Select Button


        select_button = QPushButton(

            "Become Manager"

        )


        select_button.clicked.connect(

            self.select_club

        )


        layout.addWidget(

            select_button

        )



        # Back Button


        back_button = QPushButton(

            "Back"

        )


        back_button.clicked.connect(

            lambda:

            self.controller.show_screen(

                "main_menu"

            )

        )


        layout.addWidget(

            back_button

        )



    # ======================================================
    # LOAD CLUBS
    ======================================================


    def load_clubs(self):


        self.club_list.clear()



        if not self.controller.world:


            return



        self.clubs = list(

            self.controller.world.clubs.values()

        )



        for club in self.clubs:


            self.club_list.addItem(

                f"{club.name} - {club.nickname}"

            )



    # ======================================================
    # SELECT CLUB
    ======================================================


    def select_club(self):


        index = self.club_list.currentRow()



        if index < 0:


            QMessageBox.warning(

                self,

                "No Club Selected",

                "Please choose a Speedway club."

            )


            return



        club = self.clubs[index]



        self.controller.select_club(

            club

        )



        QMessageBox.information(

            self,

            "Career Started",

            f"You are now Manager of {club.name}"

        )



        self.controller.show_screen(

            "club_dashboard"

        )



    # ======================================================
    # REFRESH
    ======================================================


    def showEvent(
        self,
        event,
    ):


        self.load_clubs()
