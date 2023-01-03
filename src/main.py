import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QKeySequence
from PyQt6.QtCore import Qt
from editor import Editor
import darkdetect

basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scribbles")

        self.textarea = Editor(self)

        self.setStatusBar(QStatusBar(self))
        self.setCentralWidget(self.textarea)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setQuitOnLastWindowClosed(False)

    def focus():
        window.setWindowState(window.windowState() & ~
                              Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        window.show()
        window.activateWindow()
        window.raise_()

    if darkdetect.isLight:
        icon = "icons/icon-white.png"
    elif darkdetect.isDark:
        icon = "icons/icon-black.png"

    window.setWindowIcon(QIcon(os.path.join(basedir, icon)))

    tray = QSystemTrayIcon()
    tray.setIcon(QIcon(os.path.join(
        basedir, icon)))
    tray.setVisible(True)
    tray.activated.connect(focus)

    menu = QMenu()

    open_window = QAction("Open")
    open_window.triggered.connect(focus)
    menu.addAction(open_window)

    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    tray.setContextMenu(menu)

    window.show()
    app.exec()
