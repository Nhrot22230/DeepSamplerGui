# utils/canvas_manager.py
from typing import Any, Dict

import numpy as np
import pyqtgraph as pg
import soundfile as sf
from PyQt6.QtCore import QObject, pyqtSignal


class CanvasManager(QObject):
    selection_changed = pyqtSignal(float, float)

    def __init__(self, settings, parent=None):
        super().__init__()
        self.plot_widget = pg.PlotWidget()
        self.region = pg.LinearRegionItem()
        self.settings = settings
        self.data = None
        self.sample_rate = None
        self.parent = parent
        self._init_plot()

    def _init_plot(self):
        self.plot_widget.setLabel("left", "Amplitude")
        self.plot_widget.setLabel("bottom", "Time (s)")
        self.plot_widget.addItem(self.region)
        self.region.sigRegionChanged.connect(self._handle_region_change)

    def load_audio(self, file_path: str, metadata: Dict[str, Any]):
        with sf.SoundFile(file_path) as f:
            self.data = f.read(dtype="float32")
            self.sample_rate = f.samplerate

        time = np.arange(len(self.data)) / self.sample_rate
        self.plot_widget.plot(time, self.data, clear=True)
        self.region.setRegion([0, len(self.data) / self.sample_rate])

    def _handle_region_change(self):
        start, end = self.region.getRegion()
        self.selection_changed.emit(start, end)
