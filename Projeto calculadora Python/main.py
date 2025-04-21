import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QIcon

from main_window import MainWindow, ButtonsGrid
from variables import WINDOW_ICON_PATH
from components import Display, Info, Button, setupTheme

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme(app=app)

    window = MainWindow()

    # Icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info()
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Buttons Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.addGridToVLayout(buttonsGrid)

    window.adjustFixedSize()

    window.show()
    app.exec()


