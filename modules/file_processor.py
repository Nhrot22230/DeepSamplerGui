# utils/file_processor.py
import os
from typing import Any, Dict, List

from mutagen import File
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

SUPPORTED_FORMATS = {"mp3", "flac", "wav"}


class FileProcessor(QObject):
    progress_updated = pyqtSignal(int, str)
    processing_finished = pyqtSignal(str, object)
    error_occurred = pyqtSignal(str)

    @pyqtSlot(list)
    def process_files(self, files: List[str]) -> None:
        try:
            for file_path in files:
                if not self._validate_file(file_path):
                    continue

                metadata = self._extract_metadata(file_path)
                self.processing_finished.emit(file_path, metadata)

        except Exception as e:
            self.error_occurred.emit(str(e))

    def _validate_file(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1][1:].lower()
        if ext not in SUPPORTED_FORMATS:
            self.error_occurred.emit(f"Unsupported file format: {ext}")
            return False
        return True

    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        metadata = {}
        try:
            audio_file = File(file_path)
            metadata = {
                "path": file_path,
                "format": audio_file.mime[0] if audio_file.mime else "",
                "duration": audio_file.info.length,
                "bitrate": getattr(audio_file.info, "bitrate", 0),
                "tags": dict(audio_file.tags) if audio_file.tags else {},
            }
        except Exception as e:
            self.error_occurred.emit(f"Metadata error: {str(e)}")
        return metadata
