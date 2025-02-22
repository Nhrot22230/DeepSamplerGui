# core/main_window.py
from typing import List, Dict, Any
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QWidget
from core.settings import AppSettings
from gui.toolbar.main_toolbar import MainToolBar
from gui.widgets.drag_drop import DragDropWidget
from gui.widgets.progress import ProgressWindow
from gui.views.audio_analysis import AudioAnalysisView
from utils.audio_processor import AudioProcessor
from utils.file_processor import FileProcessor


class MainWindow(QMainWindow):
    theme_updated = pyqtSignal(str)

    def __init__(self, settings: AppSettings) -> None:
        super().__init__()
        self.settings = settings
        self.current_view: QWidget = None
        self._init_workers()
        self._init_ui()
        self._setup_window()
        self._connect_signals()

    def _setup_window(self) -> None:
        self.setWindowTitle("Audio Separation GUI")
        self.setFixedSize(800, 600)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint
        )
        self._apply_theme()

    def _init_ui(self) -> None:
        # Toolbar
        self.toolbar = MainToolBar(self.settings, self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # Initial view
        self._show_home_view()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Progress window
        self.progress_window = ProgressWindow(self)

    def _init_workers(self) -> None:
        self.file_processor = FileProcessor(self.settings)
        self.audio_processor = AudioProcessor(self.settings)

        # Thread setup
        self.file_thread = QThread()
        self.audio_thread = QThread()
        self.file_processor.moveToThread(self.file_thread)
        self.audio_processor.moveToThread(self.audio_thread)
        self.file_thread.start()
        self.audio_thread.start()

    def _connect_signals(self) -> None:
        # File processing
        self.file_processor.progress_updated.connect(self._update_progress)
        self.file_processor.processing_finished.connect(self._handle_processing_done)
        self.file_processor.error_occurred.connect(self._handle_error)

        # Audio processing
        self.audio_processor.conversion_finished.connect(self._handle_conversion)
        self.audio_processor.error_occurred.connect(self._handle_error)

        # Settings
        self.settings.theme_changed.connect(self._apply_theme)
        self.toolbar.theme_changed.connect(self.settings.set_theme)

    def _show_home_view(self) -> None:
        self.current_view = DragDropWidget(self.settings)
        self.current_view.filesDropped.connect(self._handle_file_drop)
        self.setCentralWidget(self.current_view)

    def _show_analysis_view(self, metadata: Dict[str, Any]) -> None:
        self.current_view = AudioAnalysisView(metadata, self.settings, self)
        self.current_view.canvas.selection_changed.connect(self._handle_selection)
        self.setCentralWidget(self.current_view)

    def _apply_theme(self) -> None:
        theme = self.settings.get_theme()
        self.setStyleSheet(theme)
        self.theme_updated.emit(theme)

    def _handle_file_drop(self, files: List[str]) -> None:
        self.progress_window.show()
        self.file_processor.process_files.emit(files)

    def _update_progress(self, value: int, message: str) -> None:
        self.progress_window.update_progress(value, message)
        self.status_bar.showMessage(message)

    def _handle_processing_done(self, file_path: str, metadata: Dict[str, Any]) -> None:
        self.audio_processor.convert_to_wav.emit(file_path, metadata)

    def _handle_conversion(self, file_path: str, metadata: Dict[str, Any]) -> None:
        self.progress_window.hide()
        self._show_analysis_view(metadata)
        self.current_view.canvas.load_audio(file_path, metadata)

    def _handle_error(self, message: str) -> None:
        self.progress_window.hide()
        self.status_bar.showMessage(f"Error: {message}", 5000)

    def _handle_selection(self, start: float, end: float) -> None:
        self.status_bar.showMessage(f"Selected: {start:.2f}s - {end:.2f}s", 3000)

    def closeEvent(self, event) -> None:
        self.file_thread.quit()
        self.audio_thread.quit()
        self.file_thread.wait()
        self.audio_thread.wait()
        super().closeEvent(event)
