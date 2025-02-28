from PyQt6.QtWidgets import (
    QToolBar,
    QComboBox,
    QPushButton,
)
from modules.model_manager import ModelManager


class CustomToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.models_list = ModelManager().available_models
        self.setMovable(False)

        self._setup_ui()

    def _setup_ui(self):
        self.new_window_button = QPushButton("New Window")
        self.addWidget(self.new_window_button)

        self.file_button = QPushButton("Select Audio File")
        self.addWidget(self.file_button)

        self.model_selector = QComboBox()
        self.model_selector.addItems(self.models_list)
        self.addWidget(self.model_selector)

        self.theme_button = QPushButton("Toggle Theme")
        self.addWidget(self.theme_button)
