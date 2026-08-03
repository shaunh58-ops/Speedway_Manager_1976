"""
British League Speedway Manager

Application Theme

Version: Alpha 0.1

Controls PySide6 visual styling.
"""


from PySide6.QtWidgets import QApplication


from core.logger import get_logger



# ==========================================================
# LOGGER
# ==========================================================

log = get_logger(
    "SpeedwayTheme"
)



# ==========================================================
# THEME CLASS
# ==========================================================


class SpeedwayTheme:


    @staticmethod
    def apply(
        app: QApplication,
    ):
        """
        Apply the Speedway Manager visual theme.
        """

        stylesheet = """

        /* =====================================
           GLOBAL APPLICATION
        ===================================== */

        QWidget {

            background-color: #121212;

            color: #FFFFFF;

            font-family: "Segoe UI";

            font-size: 14px;

        }


        /* =====================================
           MAIN HEADER
        ===================================== */

        QLabel#header {

            background-color: #8B0000;

            color: white;

            font-size: 28px;

            font-weight: bold;

            padding: 20px;

            border-bottom: 4px solid #D4AF37;

        }



        /* =====================================
           BUTTONS
        ===================================== */

        QPushButton {

            background-color: #8B0000;

            color: white;

            border-radius: 6px;

            padding: 12px;

            font-size: 16px;

            font-weight: bold;

        }



        QPushButton:hover {

            background-color: #B22222;

        }



        QPushButton:pressed {

            background-color: #5A0000;

        }



        /* =====================================
           PANELS
        ===================================== */


        QFrame {

            background-color: #1E1E1E;

            border: 1px solid #444444;

            border-radius: 8px;

        }



        /* =====================================
           TABLES
        ===================================== */


        QTableWidget {

            background-color: #181818;

            alternate-background-color: #242424;

            gridline-color: #555555;

        }



        QHeaderView::section {

            background-color: #8B0000;

            color: white;

            padding: 8px;

            font-weight: bold;

        }



        /* =====================================
           MENUS
        ===================================== */


        QMenuBar {

            background-color: #0B0B0B;

            color:white;

        }


        QMenuBar::item:selected {

            background-color:#8B0000;

        }



        /* =====================================
           STATUS BAR
        ===================================== */


        QStatusBar {

            background-color:#0B0B0B;

            color:#D4AF37;

        }


        """



        app.setStyleSheet(

            stylesheet

        )



        log.info(

            "Speedway theme applied"

        )
