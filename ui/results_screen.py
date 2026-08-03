"""
British League Speedway Manager

Results Screen

Version: Alpha 0.1

Displays completed race meeting results.
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

    "ResultsScreen"

)



# ==========================================================
# RESULTS SCREEN
# ==========================================================


class ResultsScreen(QWidget):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.result = None


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


        self.title = QLabel(

            "🏁 Meeting Complete"

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



        # Score Panel


        score_box = QGroupBox(

            "Final Score"

        )


        self.score_text = QLabel()



        score_layout = QVBoxLayout()



        score_layout.addWidget(

            self.score_text

        )



        score_box.setLayout(

            score_layout

        )


        layout.addWidget(

            score_box

        )



        # Heat Results


        heat_box = QGroupBox(

            "Heat Results"

        )


        self.heat_list = QListWidget()



        heat_layout = QVBoxLayout()



        heat_layout.addWidget(

            self.heat_list

        )



        heat_box.setLayout(

            heat_layout

        )


        layout.addWidget(

            heat_box

        )



        # Rider Performance


        rider_box = QGroupBox(

            "Rider Performance"

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



        # Return Button


        button = QPushButton(

            "Return To Dashboard"

        )


        button.clicked.connect(

            self.return_dashboard

        )


        layout.addWidget(

            button

        )



    # ======================================================
    # LOAD RESULTS
    ======================================================


    def load_results(
        self,
        result,
    ):


        self.result = result


        self.refresh()



    # ======================================================
    # REFRESH DISPLAY
    ======================================================


    def refresh(self):


        if not self.result:


            return



        self.score_text.setText(

            f"""

{self.result.home_team}

{self.result.home_points}


VS


{self.result.away_team}

{self.result.away_points}

"""

        )



        self.heat_list.clear()



        for index, heat in enumerate(

            self.result.heats,

            start=1

        ):


            self.heat_list.addItem(

                f"Heat {index}: Completed"

            )



        self.rider_list.clear()



        stats = (

            self.controller

            .get_dashboard_data()

        )



        self.rider_list.addItem(

            "Top scorer information coming soon"

        )



    # ======================================================
    # RETURN
    ======================================================


    def return_dashboard(self):


        log.info(

            "Returning to dashboard"

        )


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


        self.refresh()
