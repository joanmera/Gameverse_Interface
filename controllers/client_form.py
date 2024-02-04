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
        if self.client_id:
            self._clientHandler.update_client(
                self.client_id,
                self.id_lineEdit.text(),
                self.name_lineEdit.text(),
                self.age_lineEdit.text(),
                self.gender_lineEdit.text(),
                self.number_lineEdit.text()
            )
        else:
            self._clientHandler.create_client(
                self.id_lineEdit.text(),
                self.name_lineEdit.text(),
                self.age_lineEdit.text(),
                self.gender_lineEdit.text(),
                self.number_lineEdit.text()
            )

        self.client_saved.emit()
        self.close()


    def load_client_data(self, client_id):
        self.client_id = client_id
        client_data = self._clientHandler.get_client_by_id(client_id)
        if client_data:
            self.name_lineEdit.setText(str(client_data[1]))
            self.id_lineEdit.setText(str(client_data[2]))
            self.age_lineEdit.setText(str(client_data[3]))
            self.gender_lineEdit.setText(str(client_data[4]))
            self.number_lineEdit.setText(str(client_data[5]))

