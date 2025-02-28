# core/main_window.py
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)
from core.settings import AppSettings
from gui.widgets.setup import SetupWidget
from gui.widgets.toolbar import CustomToolBar


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings):
        super().__init__()
        self.settings = settings

        self.setWindowTitle("Music Separation App")
        self.resize(1200, 800)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        # Toolbar
        self.toolbar = CustomToolBar(self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Splitter for setup and views
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Setup widget (left side)
        self.setup_widget = SetupWidget(self.settings)
        self.splitter.addWidget(self.setup_widget)

        # Stacked widget for different views (right side)
        self.stacked_widget = QStackedWidget()
        self.splitter.addWidget(self.stacked_widget)

        # Add a placeholder view
        placeholder_view = QLabel("View content will be displayed here")
        placeholder_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(placeholder_view)

        # Set initial splitter sizes
        self.splitter.setSizes([300, 900])

        main_layout.addWidget(self.splitter)
        self.setCentralWidget(main_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _connect_signals(self):
        # Connect toolbar actions
        pass

    @pyqtSlot()
    def _show_setup(self):
        self.setup_widget.setVisible(True)
        self.status_bar.showMessage("Setup mode activated")

    @pyqtSlot()
    def _show_view(self):
        self.setup_widget.setVisible(False)
        self.status_bar.showMessage("View mode activated")

    @pyqtSlot()
    def _on_process_started(self):
        self.status_bar.showMessage("Processing started...")

    @pyqtSlot()
    def _on_process_finished(self):
        self.status_bar.showMessage("Processing finished")
