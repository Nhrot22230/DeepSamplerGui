# gui/widgets/message.py
from PyQt6.QtWidgets import QMessageBox


def show_error(message: str, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText("Error")
    msg.setInformativeText(message)
    msg.exec()
