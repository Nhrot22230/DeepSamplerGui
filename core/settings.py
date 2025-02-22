# core/settings.py
from typing import cast

from PyQt6.QtCore import QObject, QSettings


class AppSettings(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.qsettings: QSettings = QSettings("NhrotCorp", "DinoSamplerGUI")

    def get_theme(self) -> str:
        theme = cast(
            str, self.qsettings.value("theme", self._default_dark_theme(), type=str)
        )
        return theme

    def set_theme(self, theme_name: str) -> None:
        self.qsettings.setValue("theme", theme_name)
        self._load_theme_file(theme_name)

    def _default_dark_theme(self) -> str:
        return """
        /* Base styling */
        QWidget {
            background-color: #000000;
            color: #00ffff;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Main window */
        QMainWindow {
            background-color: #000000;
            border: 1px solid #00ffff;
        }

        /* Toolbar */
        QToolBar {
            background-color: #0a0a0a;
            border-bottom: 2px solid rgba(0, 255, 255, 0.3);
            padding: 4px;
            spacing: 8px;
        }

        QToolButton {
            background-color: #1a1a1a;
            border: 1px solid #00ffff;
            border-radius: 4px;
            color: #00ffff;
            padding: 6px 12px;
            margin: 2px;
        }

        QToolButton:hover {
            background-color: #002a2a;
            border: 1px solid #00ffff;
        }

        QToolButton:pressed {
            background-color: #004444;
        }

        /* Status bar */
        QStatusBar {
            background-color: #0a0a0a;
            color: #00ffff;
            border-top: 1px solid rgba(0, 255, 255, 0.2);
        }

        /* Buttons */
        QPushButton {
            background-color: #1a1a1a;
            border: 1px solid #00ffff;
            border-radius: 4px;
            color: #00ffff;
            padding: 6px 12px;
            min-width: 80px;
        }

        QPushButton:hover {
            background-color: #002a2a;
        }

        QPushButton:pressed {
            background-color: #004444;
        }

        /* Input fields */
        QLineEdit, QComboBox {
            background-color: #0a0a0a;
            border: 1px solid #008080;
            border-radius: 4px;
            padding: 6px;
            color: #00ffff;
            selection-background-color: #008080;
        }

        /* Scrollbars */
        QScrollBar:vertical {
            background: #0a0a0a;
            width: 12px;
        }

        QScrollBar::handle:vertical {
            background: #008080;
            min-height: 20px;
            border-radius: 6px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }

        /* Progress bar */
        QProgressBar {
            background-color: #0a0a0a;
            border: 1px solid #008080;
            border-radius: 4px;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: #00ffff;
            border-radius: 3px;
        }

        /* Sliders */
        QSlider::groove:horizontal {
            background: #0a0a0a;
            height: 4px;
            border-radius: 2px;
        }

        QSlider::handle:horizontal {
            background: #00ffff;
            border: 1px solid #008080;
            width: 12px;
            margin: -4px 0;
            border-radius: 6px;
        }

        QSlider::sub-page:horizontal {
            background: #008080;
        }

        /* Drop zone */
        DragDropWidget {
            background-color: #0a0a0a;
            border: 2px dashed #008080;
            border-radius: 8px;
            color: #00ffff;
            font-size: 18px;
        }

        /* Canvas styling */
        PlotWidget {
            background-color: #000000;
            border: 1px solid #008080;
        }

        /* Disabled state */
        QWidget:disabled {
            color: #008080;
            border-color: #008080;
        }

        /* Custom glow effect for active elements */
        .glow-effect {
            border: 1px solid #00ffff;
            box-shadow: 0 0 8px rgba(0, 255, 255, 0.4);
        }
    """

    def save(self) -> None:
        self.qsettings.sync()
