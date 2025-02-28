# gui/widgets/setup_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from gui.widgets.components import (
    ControlPanel,
    CyberButton,
    CyberProgressBar,
    CyberSeparator,
    CyberSlider,
    DragDropWidget,
    FileSelector,
)
from core.settings import AppSettings


class SetupWidget(QWidget):
    levels_changed = pyqtSignal(dict)

    def __init__(self, settings: AppSettings):
        super().__init__()
        self.levels = {"vocals": 50, "drums": 50, "bass": 50, "other": 50}
        self.settings = settings
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # File selection
        self.file_panel = ControlPanel("Audio Input")
        self.file_selector = FileSelector("Input File:")
        self.file_panel.addWidget(self.file_selector)

        # Drag & Drop area
        self.drop_area = DragDropWidget(placeholder_text="Drag & Drop Audio Files Here")
        self.file_panel.addWidget(self.drop_area)

        # Separation controls
        self.controls_panel = ControlPanel("Separation Controls")

        self.controls_panel.addWidget(CyberSeparator())

        self.sliders = {}
        for name in self.levels.keys():
            slider = CyberSlider(
                f"{name.capitalize()} Level", 0, 200, self.levels[name]
            )
            slider.valueChanged.connect(self._on_slider_changed)
            self.sliders[name] = slider
            self.controls_panel.addWidget(slider)

        self.controls_panel.addWidget(CyberSeparator())

        self.process_button = CyberButton("Start Separation")
        self.controls_panel.addWidget(self.process_button)

        self.progress_bar = CyberProgressBar("Separation Progress")
        self.progress_bar.setValue(0)
        self.controls_panel.addWidget(self.progress_bar)

        # Add panels to layout
        layout.addWidget(self.file_panel)
        layout.addWidget(self.controls_panel)

    def _on_slider_changed(self):
        for name, slider in self.sliders.items():
            self.levels[name] = slider.value()
        self.levels_changed.emit(self.levels)

    def get_levels(self):
        return self.levels
