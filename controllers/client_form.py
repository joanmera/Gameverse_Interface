import pathlib
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton


from models.client_model import ClientModel

class ClientForm(QWidget):
    client_saved= pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self._clientHandler = ClientModel()
        mod_path= pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/clientes_form.ui",self)
        self.saveButton.clicked.connect(lambda: self.save_client())
        self.cancelButton.clicked.connect(lambda: self.close())
        self.client_id = None

    def save_client(self):
        
            self._clientHandler.create_client(
                
                
                self.id_lineEdit.text(),
                self.name_lineEdit.text(),
                self.age_lineEdit.text(),
                self.gender_lineEdit.text(),
                self.number_lineEdit.text()
            )
            self.client_saved.emit()
            self.close()
         
        