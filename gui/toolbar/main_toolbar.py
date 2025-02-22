# gui/toolbar/main_toolbar.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar


class MainToolBar(QToolBar):
    action_triggered = pyqtSignal(str)
    theme_changed = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__("Main Toolbar", parent)
        self._init_actions()
        self._setup_style()

    def _init_actions(self):
        # Main actions with icons and tooltips
        actions = [
            ("New Window", "new_window", "Create new workspace window"),
            ("Open File", "open_file", "Open audio file from disk"),
            ("Model Settings", "model_config", "Configure separation model"),
            ("Application Settings", "app_settings", "Adjust application preferences"),
        ]

        for text, icon_name, tooltip in actions:
            action = QAction(QIcon(f":/icons/{icon_name}"), text, self)
            action.triggered.connect(self._create_dummy_handler(text))
            action.setToolTip(tooltip)
            self.addAction(action)

    def _create_dummy_handler(self, action_name: str):
        def handler():
            self.action_triggered.emit(f"{action_name} functionality coming soon!")

        return handler

    def _setup_style(self):
        self.setMovable(False)
        self.setFloatable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
