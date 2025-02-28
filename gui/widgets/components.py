# core/widgets/components.py
import os
from typing import List, Optional, Union

from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class CyberButton(QPushButton):
    """Custom styled button with optional icon."""

    def __init__(
        self,
        text: str = "",
        icon_path: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(text, parent)

        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))

        # Additional styling can be applied here if needed
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(32)


class CyberSlider(QWidget):
    """Custom slider with label and value display."""

    valueChanged = pyqtSignal(int)

    def __init__(
        self,
        title: str,
        min_val: int = 0,
        max_val: int = 100,
        default_val: int = 50,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Header with title and value
        self.header_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.value_label = QLabel(str(default_val))
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.value_label)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setValue(default_val)
        self.slider.valueChanged.connect(self._on_value_changed)

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.slider)

    def _on_value_changed(self, value: int) -> None:
        self.value_label.setText(str(value))
        self.valueChanged.emit(value)

    def value(self) -> int:
        return self.slider.value()

    def setValue(self, value: int) -> None:
        self.slider.setValue(value)


class CyberComboBox(QWidget):
    """Combo box with label."""

    currentTextChanged = pyqtSignal(str)
    currentIndexChanged = pyqtSignal(int)

    def __init__(
        self, title: str, items: List[str] = None, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(title)
        self.combo = QComboBox()

        if items:
            self.combo.addItems(items)

        self.combo.currentTextChanged.connect(self.currentTextChanged)
        self.combo.currentIndexChanged.connect(self.currentIndexChanged)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.combo)

    def addItems(self, items: List[str]) -> None:
        self.combo.addItems(items)

    def currentText(self) -> str:
        return self.combo.currentText()

    def currentIndex(self) -> int:
        return self.combo.currentIndex()

    def setCurrentIndex(self, index: int) -> None:
        self.combo.setCurrentIndex(index)


class DragDropWidget(QWidget):
    """Widget that accepts file drops."""

    filesDropped = pyqtSignal(list)

    def __init__(
        self,
        accept_extensions: List[str] = None,
        placeholder_text: str = "Drop files here",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.accept_extensions = accept_extensions or [".wav", ".mp3", ".flac"]

        self.setAcceptDrops(True)
        self.layout = QVBoxLayout(self)

        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # You would need to provide a drop icon image
        # self.icon_label.setPixmap(
        # QPixmap("path/to/drop_icon.png").
        # scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))

        self.text_label = QLabel(placeholder_text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addStretch()
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.text_label)
        self.layout.addStretch()

        self.setMinimumHeight(150)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            valid_files = self._validate_urls(event.mimeData().urls())
            if valid_files:
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            file_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if self._is_valid_file(file_path):
                    file_paths.append(file_path)

            if file_paths:
                self.filesDropped.emit(file_paths)
                event.acceptProposedAction()

    def _validate_urls(self, urls: List[QUrl]) -> bool:
        for url in urls:
            if self._is_valid_file(url.toLocalFile()):
                return True
        return False

    def _is_valid_file(self, file_path: str) -> bool:
        return any(file_path.lower().endswith(ext) for ext in self.accept_extensions)


class FileSelector(QWidget):
    """Widget for selecting files with browse button."""

    fileSelected = pyqtSignal(str)

    def __init__(
        self,
        label_text: str = "File:",
        placeholder: str = "Select a file...",
        file_filter: str = "Audio Files (*.wav *.mp3 *.flac)",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.file_filter = file_filter

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText(placeholder)
        self.file_path.setReadOnly(True)

        self.browse_button = CyberButton("Browse")
        self.browse_button.clicked.connect(self._browse_file)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_path, 1)  # Give it stretch priority
        self.layout.addWidget(self.browse_button)

    def _browse_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", self.file_filter
        )
        if file_path:
            self.file_path.setText(file_path)
            self.fileSelected.emit(file_path)

    def getFilePath(self) -> str:
        return self.file_path.text()

    def setFilePath(self, path: str) -> None:
        self.file_path.setText(path)


class CyberProgressBar(QWidget):
    """Custom progress bar with label and cancel option."""

    canceled = pyqtSignal()

    def __init__(
        self,
        title: str = "Progress",
        show_cancel: bool = True,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.header_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.percentage_label = QLabel("0%")

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.percentage_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)

        # Footer with cancel button if needed
        self.footer_layout = QHBoxLayout()
        self.footer_layout.addStretch()

        if show_cancel:
            self.cancel_button = CyberButton("Cancel")
            self.cancel_button.clicked.connect(self.canceled)
            self.footer_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.progress_bar)
        self.layout.addLayout(self.footer_layout)

    def setValue(self, value: int) -> None:
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")

    def value(self) -> int:
        return self.progress_bar.value()


class CyberSeparator(QFrame):
    """Horizontal or vertical separator line."""

    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        if orientation == Qt.Orientation.Horizontal:
            self.setFrameShape(QFrame.Shape.HLine)
        else:
            self.setFrameShape(QFrame.Shape.VLine)

        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setStyleSheet("background-color: #008080;")


class ControlPanel(QWidget):
    """Panel with title and content area for controls."""

    def __init__(self, title: str, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Title bar
        self.title_frame = QFrame()
        self.title_frame.setStyleSheet("background-color: #0a0a0a;")
        self.title_layout = QHBoxLayout(self.title_frame)
        self.title_layout.setContentsMargins(8, 4, 8, 4)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")
        self.title_layout.addWidget(self.title_label)

        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        # Add to main layout
        self.layout.addWidget(self.title_frame)
        self.layout.addWidget(self.content_widget)

        # Style
        self.setStyleSheet(
            """
            ControlPanel {
                border: 1px solid #008080;
                border-radius: 4px;
                background-color: #0a0a0a;
            }
        """
        )

    def addWidget(self, widget: QWidget) -> None:
        self.content_layout.addWidget(widget)

    def addLayout(self, layout: Union[QHBoxLayout, QVBoxLayout]) -> None:
        self.content_layout.addLayout(layout)

    def addSpacing(self, spacing: int) -> None:
        self.content_layout.addSpacing(spacing)

    def addStretch(self, stretch: int = 1) -> None:
        self.content_layout.addStretch(stretch)
