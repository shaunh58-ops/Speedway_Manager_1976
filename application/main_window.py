"""
British League Speedway Manager

Main Window

Version: Alpha 0.1

Primary PySide6 application container.
"""


from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QStatusBar
)


from PySide6.QtCore import Qt



from core.logger import get_logger



from ui.main_menu import MainMenu



log = get_logger(
    "MainWindow"
)



# ==========================================================
# MAIN WINDOW
# ==========================================================


class MainWindow(QMainWindow):


    def __init__(
        self,
        controller,
    ):


        super().__init__()


        self.controller = controller


        self.controller.attach_window(

            self

        )


        self.screens = {}



        self.configure_window()


        self.setup_ui()


        self.load_screens()


        self.show_initial_screen()



        log.info(
            "Main window initialised"
        )



    # ======================================================
    # WINDOW CONFIGURATION
    # ======================================================


    def configure_window(self):


        self.setWindowTitle(

            "British League Speedway Manager - 1976"

        )


        self.resize(

            1400,

            900

        )


        self.setMinimumSize(

            1100,

            700

        )



    # ======================================================
    # BUILD UI
    ======================================================


    def setup_ui(self):


        container = QWidget()



        layout = QVBoxLayout()



        container.setLayout(

            layout

        )



        self.setCentralWidget(

            container

        )



        # Header

        self.header = QLabel(

            "🏁 British League Speedway Manager 1976"

        )


        self.header.setAlignment(

            Qt.AlignCenter

        )


        self.header.setObjectName(

            "header"

        )


        layout.addWidget(

            self.header

        )



        # Screen container


        self.screen_stack = QStackedWidget()



        layout.addWidget(

            self.screen_stack

        )



        # Status


        self.status_bar = QStatusBar()



        self.setStatusBar(

            self.status_bar

        )


        self.status_bar.showMessage(

            "Ready"

        )



    # ======================================================
    # LOAD SCREENS
    ======================================================


    def load_screens(self):


        log.info(

            "Loading application screens"

        )



        self.register_screen(

            "main_menu",

            MainMenu(

                self.controller

            )

        )



    # ======================================================
    # REGISTER SCREEN
    ======================================================


    def register_screen(
        self,
        name,
        widget,
    ):


        self.screens[name] = widget



        self.screen_stack.addWidget(

            widget

        )



        widget.setObjectName(

            name

        )



        log.info(

            f"Registered screen: {name}"

        )



    # ======================================================
    # SHOW SCREEN
    ======================================================


    def show_screen(
        self,
        name,
    ):


        if name not in self.screens:


            log.error(

                f"Screen not found: {name}"

            )


            return



        self.screen_stack.setCurrentWidget(

            self.screens[name]

        )


        log.info(

            f"Showing screen: {name}"

        )



    # ======================================================
    # INITIAL SCREEN
    ======================================================


    def show_initial_screen(self):


        self.show_screen(

            "main_menu"

        )


    # ======================================================
    # STATUS UPDATE
    ======================================================


    def update_status(
        self,
        message,
    ):


        self.status_bar.showMessage(

            message

        )
