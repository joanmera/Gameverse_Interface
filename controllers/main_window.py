from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton
from PyQt5 import uic
import pathlib
from PyQt5 import QtCore

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/MainWindow.ui", self)

        
