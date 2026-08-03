"""
British League Speedway Manager

Main Menu Screen

Version: Alpha 0.1

First user interface screen.
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)


from PySide6.QtCore import Qt



from core.logger import get_logger



log = get_logger(

    "MainMenu"

)



# ==========================================================
# MAIN MENU SCREEN
# ==========================================================


class MainMenu(QWidget):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.setup_ui()



    # ======================================================
    # CREATE UI
    # ======================================================


    def setup_ui(self):


        layout = QVBoxLayout()



        layout.setAlignment(

            Qt.AlignCenter

        )



        self.setLayout(

            layout

        )



        # ----------------------------------
        # Title
        # ----------------------------------


        title = QLabel(

            "🏁\n"
            "British League Speedway Manager\n"
            "1976"

        )


        title.setAlignment(

            Qt.AlignCenter

        )


        title.setObjectName(

            "main_title"

        )



        layout.addWidget(

            title

        )



        # ----------------------------------
        # New Game Button
        # ----------------------------------


        new_game = QPushButton(

            "🏆 New Game"

        )


        new_game.clicked.connect(

            self.start_new_game

        )


        layout.addWidget(

            new_game

        )



        # ----------------------------------
        # Load Game
        # ----------------------------------


        load_game = QPushButton(

            "📂 Load Game"

        )


        load_game.clicked.connect(

            self.load_game

        )


        layout.addWidget(

            load_game

        )



        # ----------------------------------
        # Options
        # ----------------------------------


        options = QPushButton(

            "⚙ Options"

        )


        options.clicked.connect(

            self.show_options

        )


        layout.addWidget(

            options

        )



        # ----------------------------------
        # Exit
        # ----------------------------------


        exit_button = QPushButton(

            "❌ Exit"

        )


        exit_button.clicked.connect(

            self.exit_game

        )


        layout.addWidget(

            exit_button

        )



    # ======================================================
    # BUTTON ACTIONS
    # ======================================================


    def start_new_game(self):


        log.info(

            "New game selected"

        )



        world = self.controller.new_game()



        if world:


            QMessageBox.information(

                self,

                "New Season",

                "1976 Speedway Season Created"

            )



            # Club selection screen
            # will be opened here next.



    # ======================================================


    def load_game(self):


        log.info(

            "Load game selected"

        )



        self.controller.load_game()



    # ======================================================


    def show_options(self):


        QMessageBox.information(

            self,

            "Options",

            "Options menu coming soon."

        )



    # ======================================================


    def exit_game(self):


        self.controller.exit_game()
