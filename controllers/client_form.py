import pathlib
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton


from models.client_model import ClientModel

class ClientForm(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._client_model = ClientModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/clientes.ui", self)
        
    def load_client(self):
        client_list = self._client_model.get_clients()
        self.clientTable.setRowCount(len(client_list))
        for i, client in enumerate(client_list):
            id_cliente, cedula, edad, genero, telefono = client
            self.clientTable.setItem(i, 0, QTableWidgetItem(str(id_cliente)))
            self.clientTable.setItem(i, 1, QTableWidgetItem(str(cedula)))
            self.clientTable.setItem(i, 2, QTableWidgetItem(str(edad)))
            self.clientTable.setItem(i, 3, QTableWidgetItem(str(genero)))
            self.clientTable.setItem(i, 4, QTableWidgetItem(str(telefono)))
        
        