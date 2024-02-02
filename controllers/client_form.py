import pathlib
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton


from models.client_model import ClientModel

class ClientForm(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._studentHandler = ClientModel()
        mod_path= pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/clientes.ui",self)
        
        