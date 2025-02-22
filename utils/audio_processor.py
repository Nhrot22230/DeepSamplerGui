# utils/audio_processor.py
import ffmpeg
import soundfile as sf
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class AudioProcessor(QObject):
    conversion_finished = pyqtSignal(str, object)
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    @pyqtSlot(str)
    def convert_to_wav(self, input_path: str) -> None:
        try:
            output_path = input_path.rsplit(".", 1)[0] + ".wav"

            # FFmpeg conversion
            (
                ffmpeg.input(input_path)
                .output(output_path, acodec="pcm_s16le", ar="44100")
                .run(quiet=True)
            )

            # Metadata extraction
            with sf.SoundFile(output_path) as f:
                metadata = {
                    "duration": len(f) / f.samplerate,
                    "sample_rate": f.samplerate,
                    "channels": f.channels,
                    "samples": len(f),
                }

            self.conversion_finished.emit(output_path, metadata)

        except Exception as e:
            self.error_occurred.emit(str(e))
