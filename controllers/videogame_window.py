import pathlib
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton


from models.client_model import ClientModel
from controllers.client_form import ClientForm

class VideogameWinindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.__model = ClientModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/clientes.ui", self)
        self._new_client = ClientForm()
        self.load_client()
        self.newClientAction.triggered.connect(lambda: self.create_client())
        self._new_client.client_saved.connect(self.load_client)
    
        
    def load_client(self):
        client_list = self._client_model.get_clients()
        self.clientTable.setRowCount(len(client_list))
        for i, cliente in enumerate(client_list):
            id_cliente, nombre_cliente, cedula, edad, genero, telefono = cliente
            self.clientTable.setItem(i, 0, QTableWidgetItem(str(id_cliente)))
            self.clientTable.setItem(i, 1, QTableWidgetItem(str(nombre_cliente)))
            self.clientTable.setItem(i, 2, QTableWidgetItem(str(cedula)))
            self.clientTable.setItem(i, 3, QTableWidgetItem(str(edad)))
            self.clientTable.setItem(i, 4, QTableWidgetItem(str(genero)))
            self.clientTable.setItem(i, 5, QTableWidgetItem(str(telefono)))


            edit_button = QPushButton ("Editar")
            edit_button.clicked.connect(self.edit_client)
            edit_button.setProperty("row", i)
            self.clientTable.setCellWidget(i, 6, edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(self.delete_client)
            delete_button.setProperty("row", i)
            self.clientTable.setCellWidget(i, 7, delete_button)


    def edit_client(self):
        sender = self.sender()
        row = sender.property("row")
        student_id = self.clientTable.item(row, 0).text()
        self._new_client.load_client_data(student_id)
        self._new_client.show()
    
    def delete_client(self):
        sender = self.sender()
        row = sender.property("row")
        client_id = self.clientTable.item(row, 0).text()

        reply = QMessageBox.question(self, 'Eliminar Cliente', '¿Estás seguro de que deseas eliminar este cliente?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._client_model.delete_client(client_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Cliente eliminado correctamente.')
                self.load_client()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar el cliente.')

    def create_client(self):
        self._new_client.reset_form()
        self._new_client.show()

    def closeEvent(self, ev) -> None:
        self._client_model.close()
        return super().closeEvent(ev)