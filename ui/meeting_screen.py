"""
British League Speedway Manager

Meeting Screen

Version: Alpha 0.1

Race meeting preparation interface.
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox
)


from PySide6.QtCore import Qt


from core.logger import get_logger



log = get_logger(
    "MeetingScreen"
)



# ==========================================================
# MEETING SCREEN
# ==========================================================


class MeetingScreen(QWidget):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.fixture = None


        self.setup_ui()



    # ======================================================
    # CREATE UI
    # ======================================================


    def setup_ui(self):


        layout = QVBoxLayout()



        self.setLayout(

            layout

        )



        # Header

        self.title = QLabel()



        self.title.setAlignment(

            Qt.AlignCenter

        )


        self.title.setObjectName(

            "screen_title"

        )


        layout.addWidget(

            self.title

        )



        # Match Information


        self.match_box = QGroupBox(

            "Meeting Information"

        )


        self.match_text = QLabel()



        box_layout = QVBoxLayout()



        box_layout.addWidget(

            self.match_text

        )



        self.match_box.setLayout(

            box_layout

        )


        layout.addWidget(

            self.match_box

        )



        # Conditions


        self.conditions_box = QGroupBox(

            "Race Conditions"

        )


        self.conditions_text = QLabel()



        condition_layout = QVBoxLayout()



        condition_layout.addWidget(

            self.conditions_text

        )



        self.conditions_box.setLayout(

            condition_layout

        )


        layout.addWidget(

            self.conditions_box

        )



        # Buttons


        lineup_button = QPushButton(

            "👥 Confirm Line-up"

        )


        lineup_button.clicked.connect(

            self.confirm_lineup

        )


        layout.addWidget(

            lineup_button

        )



        start_button = QPushButton(

            "🏁 Start Meeting"

        )


        start_button.clicked.connect(

            self.start_meeting

        )


        layout.addWidget(

            start_button

        )



        back_button = QPushButton(

            "⬅ Back"

        )


        back_button.clicked.connect(

            self.back

        )


        layout.addWidget(

            back_button

        )



    # ======================================================
    # LOAD MEETING
    # ======================================================


    def load_meeting(self):


        club = self.controller.get_current_club()



        if not club:

            return



        fixtures = [

            fixture

            for fixture

            in self.controller.world.fixtures.values()

            if fixture.home_team == club.name

            or fixture.away_team == club.name

        ]



        if fixtures:


            self.fixture = fixtures[0]



        self.refresh()



    # ======================================================
    # REFRESH DISPLAY
    # ======================================================


    def refresh(self):


        if not self.fixture:


            self.title.setText(

                "No Meeting Selected"

            )

            return



        self.title.setText(

            f"🏁 {self.fixture.home_team} vs "
            f"{self.fixture.away_team}"

        )



        self.match_text.setText(

            f"""

Date:

{self.fixture.date}


Venue:

{self.fixture.venue}

"""

        )



        self.conditions_text.setText(

            """

Weather:

Dry


Temperature:

18°C


Track:

Fast

"""

        )



    # ======================================================
    # ACTIONS
    ======================================================


    def confirm_lineup(self):


        log.info(

            "Line-up confirmed"

        )



    # ------------------------------------------------------


    def start_meeting(self):


        log.info(

            "Starting race meeting"

        )


        self.controller.show_screen(

            "race_screen"

        )



    # ------------------------------------------------------


    def back(self):


        self.controller.show_screen(

            "club_dashboard"

        )



    # ======================================================
    # SHOW EVENT
    ======================================================


    def showEvent(
        self,
        event,
    ):


        self.load_meeting()
