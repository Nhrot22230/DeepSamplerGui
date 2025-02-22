# gui/views/audio_analysis.py
from typing import Any, Dict

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from core.settings import AppSettings
from utils.canvas_manager import CanvasManager


class AudioAnalysisView(QWidget):
    def __init__(self, metadata: Dict[str, Any], settings: AppSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.metadata = metadata
        self.canvas = CanvasManager(settings)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self) -> None:
        layout = QVBoxLayout()

        # Metadata panel
        meta_layout = QHBoxLayout()
        meta_layout.addWidget(QLabel(f"Duration: {self.metadata['duration']:.2f}s"))
        meta_layout.addWidget(QLabel(f"Sample Rate: {self.metadata['sample_rate']}Hz"))
        meta_layout.addWidget(QLabel(f"Channels: {self.metadata['channels']}"))
        layout.addLayout(meta_layout)

        # Canvas
        layout.addWidget(self.canvas.plot_widget)
        self.setLayout(layout)

    def _connect_signals(self) -> None:
        self.settings.theme_changed.connect(self._update_theme)

    def _update_theme(self) -> None:
        self.canvas.apply_theme(self.settings.get_theme())
