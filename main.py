# main.py
from core.app import MusicSeparationApp
from modules.model_manager import ModelManager

if __name__ == "__main__":
    model_manager = ModelManager()
    app = MusicSeparationApp()
    app.run()
