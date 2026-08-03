"""
British League Speedway Manager

Race Screen

Version: Alpha 0.1

Live heat racing interface.
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QGroupBox
)


from PySide6.QtCore import Qt


from core.logger import get_logger



log = get_logger(

    "RaceScreen"

)



# ==========================================================
# RACE SCREEN
# ==========================================================


class RaceScreen(QWidget):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.current_heat = 1


        self.total_heats = 15


        self.setup_ui()



    # ======================================================
    # CREATE UI
    ======================================================


    def setup_ui(self):


        layout = QVBoxLayout()



        self.setLayout(

            layout

        )



        # Header


        self.title = QLabel(

            "🏁 Race Meeting"

        )


        self.title.setAlignment(

            Qt.AlignCenter

        )


        self.title.setObjectName(

            "screen_title"

        )


        layout.addWidget(

            self.title

        )



        # Heat Information


        self.heat_label = QLabel()



        self.heat_label.setAlignment(

            Qt.AlignCenter

        )


        layout.addWidget(

            self.heat_label

        )



        # Riders


        rider_box = QGroupBox(

            "Starting Gate"

        )


        self.rider_list = QListWidget()



        rider_layout = QVBoxLayout()



        rider_layout.addWidget(

            self.rider_list

        )



        rider_box.setLayout(

            rider_layout

        )


        layout.addWidget(

            rider_box

        )



        # Commentary


        commentary_box = QGroupBox(

            "Live Commentary"

        )


        self.commentary = QLabel()



        self.commentary.setWordWrap(

            True

        )



        commentary_layout = QVBoxLayout()



        commentary_layout.addWidget(

            self.commentary

        )



        commentary_box.setLayout(

            commentary_layout

        )


        layout.addWidget(

            commentary_box

        )



        # Button


        self.start_button = QPushButton(

            "🏁 Start Heat"

        )


        self.start_button.clicked.connect(

            self.run_heat

        )


        layout.addWidget(

            self.start_button

        )



        # Back


        back_button = QPushButton(

            "⬅ Return"

        )


        back_button.clicked.connect(

            self.back

        )


        layout.addWidget(

            back_button

        )



    # ======================================================
    # LOAD HEAT
    ======================================================


    def load_heat(self):


        self.heat_label.setText(

            f"Heat {self.current_heat} / {self.total_heats}"

        )



        self.rider_list.clear()



        riders = [

            "Rider 1",

            "Rider 2",

            "Rider 3",

            "Rider 4"

        ]



        for rider in riders:


            self.rider_list.addItem(

                rider

            )



        self.commentary.setText(

            "Riders approach the starting gate..."

        )



    # ======================================================
    # SIMULATE HEAT
    ======================================================


    def run_heat(self):


        log.info(

            f"Running heat {self.current_heat}"

        )


        self.commentary.setText(

            """

The tapes rise!


The riders explode from the gate!


Entering the first bend...


Heat complete.

"""

        )


        self.start_button.setText(

            "Next Heat"

        )


        self.start_button.clicked.disconnect()



        self.start_button.clicked.connect(

            self.next_heat

        )



    # ======================================================
    # NEXT HEAT
    ======================================================


    def next_heat(self):


        self.current_heat += 1



        if self.current_heat > self.total_heats:


            self.finish_meeting()

            return



        self.start_button.setText(

            "🏁 Start Heat"

        )


        self.start_button.clicked.disconnect()



        self.start_button.clicked.connect(

            self.run_heat

        )


        self.load_heat()



    # ======================================================
    # FINISH MEETING
    ======================================================


    def finish_meeting(self):


        log.info(

            "Meeting complete"

        )


        self.commentary.setText(

            "Meeting Complete - Processing Results"

        )



    # ======================================================
    # RETURN
    ======================================================


    def back(self):


        self.controller.show_screen(

            "meeting_screen"

        )



    # ======================================================
    # DISPLAY
    ======================================================


    def showEvent(
        self,
        event,
    ):


        self.current_heat = 1


        self.load_heat()
