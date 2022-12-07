from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QKeySequence, QShortcut
from datetime import datetime
import os


class Editor(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.path = os.path.expanduser("~/Desktop")
        self.filename = None
        self.setAcceptDrops(True)

        save_shortcut = QShortcut(QKeySequence("CTRL+S"), self)
        save_shortcut.activated.connect(self.save)
        new_shortcut = QShortcut(QKeySequence("CTRL+N"), self)
        new_shortcut.activated.connect(self.new)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.open(f)

    def open(self, file):
        with open(file, "r") as f:
            self.setPlainText(f.read())
        self.filename = file

    def save(self):
        if not self.filename:
            self.filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".txt"

        with open(os.path.join(self.path, self.filename), "w") as f:
            f.write(self.toPlainText())
        self.parent.statusBar().showMessage(
            f"Note saved ({self.filename})", 2000)

    def new(self):
        self.filename = None
        self.setPlainText("")
