from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout


class ProgressWindow(QDialog):
    """
    A simple progress window/dialog to indicate that a background process is running.
    """

    def __init__(self, title="Processing", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Please wait...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_progress(self, value: int):
        """
        Update the progress bar to a new value.
        """
        self.progress_bar.setValue(value)
