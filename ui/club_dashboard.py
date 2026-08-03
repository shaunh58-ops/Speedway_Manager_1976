"""
British League Speedway Manager

Club Dashboard Screen

Version: Alpha 0.1

Main player management interface.
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

    "ClubDashboard"

)



# ==========================================================
# CLUB DASHBOARD
# ==========================================================


class ClubDashboard(QWidget):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.setup_ui()



    # ======================================================
    # CREATE UI
    ======================================================


    def setup_ui(self):


        layout = QVBoxLayout()



        self.setLayout(

            layout

        )



        # ----------------------------------
        # Club Header
        # ----------------------------------


        self.club_title = QLabel()



        self.club_title.setAlignment(

            Qt.AlignCenter

        )


        self.club_title.setObjectName(

            "screen_title"

        )


        layout.addWidget(

            self.club_title

        )



        # ----------------------------------
        # Club Information
        # ----------------------------------


        self.info_panel = QGroupBox(

            "Club Information"

        )


        self.info_text = QLabel()



        info_layout = QVBoxLayout()



        info_layout.addWidget(

            self.info_text

        )



        self.info_panel.setLayout(

            info_layout

        )



        layout.addWidget(

            self.info_panel

        )



        # ----------------------------------
        # Next Fixture
        # ----------------------------------


        self.fixture_panel = QGroupBox(

            "Next Fixture"

        )


        self.fixture_text = QLabel()



        fixture_layout = QVBoxLayout()



        fixture_layout.addWidget(

            self.fixture_text

        )



        self.fixture_panel.setLayout(

            fixture_layout

        )



        layout.addWidget(

            self.fixture_panel

        )



        # ----------------------------------
        # Buttons
        # ----------------------------------


        team_button = QPushButton(

            "👥 View Team"

        )


        team_button.clicked.connect(

            self.view_team

        )


        layout.addWidget(

            team_button

        )



        meeting_button = QPushButton(

            "🏁 Start Race Meeting"

        )


        meeting_button.clicked.connect(

            self.start_meeting

        )


        layout.addWidget(

            meeting_button

        )



        table_button = QPushButton(

            "🏆 League Table"

        )


        table_button.clicked.connect(

            self.show_table

        )


        layout.addWidget(

            table_button

        )



        save_button = QPushButton(

            "💾 Save Game"

        )


        save_button.clicked.connect(

            self.save_game

        )


        layout.addWidget(

            save_button

        )



    # ======================================================
    # REFRESH DATA
    ======================================================


    def refresh(self):


        club = self.controller.get_current_club()



        if not club:


            self.club_title.setText(

                "No Club Selected"

            )

            return



        self.club_title.setText(

            f"🏁 {club.name}"

        )



        self.info_text.setText(

            f"""

Venue:

{club.venue}


Riders:

{len(club.riders)}


Season:

1976 British League

"""

        )



        self.load_next_fixture()



    # ======================================================
    # NEXT FIXTURE
    ======================================================


    def load_next_fixture(self):


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


            fixture = fixtures[0]


            self.fixture_text.setText(

                f"""

{fixture.home_team}

vs

{fixture.away_team}


Date:

{fixture.date}


Venue:

{fixture.venue}

"""

            )


        else:


            self.fixture_text.setText(

                "No Fixtures Found"

            )



    # ======================================================
    # ACTIONS
    ======================================================


    def view_team(self):


        log.info(

            "Team view selected"

        )



    # ------------------------------------------------------


    def start_meeting(self):


        log.info(

            "Starting meeting"

        )


        self.controller.show_screen(

            "meeting_screen"

        )



    # ------------------------------------------------------


    def show_table(self):


        log.info(

            "League table selected"

        )



    # ------------------------------------------------------


    def save_game(self):


        self.controller.save_game()



    # ======================================================
    # DISPLAY EVENT
    ======================================================


    def showEvent(
        self,
        event,
    ):


        self.refresh()
