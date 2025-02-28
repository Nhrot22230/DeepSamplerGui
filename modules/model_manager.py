import torch
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot


# Dummy model classes for demonstration.
class ModelA(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)


# Worker object that executes a function in a separate thread.
class Worker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# Simplified ModelManager focused only on model operations
class ModelManager(QObject):
    # Signals for notifying the application about operation results
    model_loaded = pyqtSignal(object)
    model_run_finished = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Dictionary mapping model names to model classes
        self.available_models = {
            "ModelA": ModelA,
            "ModelB": ModelA,
            "ModelC": ModelA,
        }
        self.model = None

    def get_available_models(self):
        """Return a list of available model names."""
        return list(self.available_models.keys())

    def _run_in_thread(self, func, *args, **kwargs):
        """Helper method to run a function in a separate thread."""
        thread = QThread()
        worker = Worker(func, *args, **kwargs)
        worker.moveToThread(thread)

        # Connect signals
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(self.error_occurred)
        worker.error.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)

        thread.start()
        return worker

    def build_model(self, model_name):
        """Build a model by name."""

        def _build():
            if model_name not in self.available_models:
                raise ValueError(f"Model '{model_name}' is not available.")
            model_class = self.available_models[model_name]
            model = model_class()
            self.model = model
            return model

        worker = self._run_in_thread(_build)
        worker.finished.connect(self.model_loaded)

    def load_checkpoint(self, model_path):
        """Load a model from a checkpoint file."""

        def _load():
            model = torch.jit.load(model_path)
            self.model = model
            return model

        worker = self._run_in_thread(_load)
        worker.finished.connect(self.model_loaded)

    def run_model(self, input_data):
        """Run the model with the given input data."""

        def _run():
            if self.model is None:
                raise RuntimeError("No model loaded.")
            return self.model(input_data)

        worker = self._run_in_thread(_run)
        worker.finished.connect(self.model_run_finished)
