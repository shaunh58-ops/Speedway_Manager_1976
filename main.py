"""
British League Speedway Manager

Application Entry Point

Version: Alpha 0.1

Starts the PySide6 desktop application.
"""


import sys


from PySide6.QtWidgets import QApplication


from application.main_window import MainWindow


from application.theme import SpeedwayTheme


from application.application_controller import ApplicationController


from core.logger import get_logger



# ==========================================================
# LOGGER
# ==========================================================

log = get_logger(
    "Application"
)



# ==========================================================
# APPLICATION STARTUP
# ==========================================================


def create_application():

    """
    Creates and configures the Qt application.
    """


    app = QApplication(sys.argv)


    app.setApplicationName(
        "British League Speedway Manager"
    )


    app.setApplicationVersion(
        "Alpha 0.1"
    )


    app.setOrganizationName(
        "Speedway Manager Project"
    )


    # Apply visual theme

    SpeedwayTheme.apply(app)


    return app



# ==========================================================
# MAIN APPLICATION
# ==========================================================


def main():


    log.info(
        "Starting Speedway Manager Application"
    )


    app = create_application()



    # Create game controller

    controller = ApplicationController()



    # Create main window

    window = MainWindow(

        controller

    )


    window.show()



    log.info(
        "Application started successfully"
    )



    return app.exec()



# ==========================================================
# PROGRAM ENTRY
# ==========================================================


if __name__ == "__main__":


    sys.exit(

        main()

    )
