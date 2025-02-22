# core/app.py
import sys

from PyQt6.QtWidgets import QApplication

from core.main_window import MainWindow
from core.settings import AppSettings


class MusicSeparationApp:
    def __init__(self) -> None:
        self.qapp = QApplication(sys.argv)
        self.settings = AppSettings()
        self.main_window = MainWindow(self.settings)
        self._apply_theme()

    def _apply_theme(self) -> None:
        theme = self.settings.get_theme()
        self.qapp.setStyleSheet(theme)

    def run(self) -> int:
        self.main_window.show()
        return self.qapp.exec()
